import json
import os
from airflow.decorators import dag, task
from datetime import datetime
from airflow.providers.postgres.operators import postgres

# Define o ID da conexão a ser usada em toda a DAG
POSTGRES_CONN_ID = "postgres_default"

@dag(
    dag_id="imoveis_etl_pipeline",
    start_date=datetime(2023, 1, 1),
    schedule=None,
    catchup=False,
    tags=["imoveis", "etl"],
    doc_md="""
    ### Pipeline de ETL de Imóveis
    Esta DAG realiza o ETL de dados de imóveis.
    1. **Cria Tabela**: Garante que a tabela de destino 'imoveis' exista no PostgreSQL.
    2. **Carrega Dados**: Lê dados de um arquivo JSON, limpa os valores e os insere na tabela.
    """
)
def imoveis_etl_dag():
    """
    Define o pipeline de ETL com duas tarefas: criar a tabela e carregar os dados.
    """

    # Tarefa 1: Criar a tabela usando PostgresOperator
    # O comando 'CREATE TABLE IF NOT EXISTS' é idempotente, ou seja,
    # só cria a tabela se ela não existir, evitando erros em execuções futuras.
    create_imoveis_table = postgres.PostgresOperator(
        task_id="create_imoveis_table",
        postgres_conn_id=POSTGRES_CONN_ID,
        sql="""
            CREATE TABLE IF NOT EXISTS imoveis (
                card VARCHAR(255) PRIMARY KEY,
                url TEXT,
                endereco TEXT,
                tipo_imovel VARCHAR(255),
                aluguel NUMERIC(10, 2),
                condominio NUMERIC(10, 2),
                iptu NUMERIC(10, 2),
                total NUMERIC(10, 2),
                last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """
    )

    @task
    def run_load():
        """
        Esta tarefa lê dados de um arquivo JSON e os carrega no PostgreSQL.
        """
        from airflow.providers.postgres.hooks.postgres import PostgresHook

        def limpar(valor):
            if valor in (None, "---"): return None
            valor = str(valor).replace("R$", "").replace("\xa0", " ").replace(".", "").replace(",", ".").strip()
            try:
                return float(valor)
            except (ValueError, TypeError):
                return None

        AIRFLOW_HOME = os.getenv("AIRFLOW_HOME", "/usr/local/airflow")
        data_path = os.path.join(AIRFLOW_HOME, "include", "data", "resultados_clean.json")

        with open(data_path, "r", encoding="utf-8") as f:
            dados = json.load(f)

        pg_hook = PostgresHook(postgres_conn_id=POSTGRES_CONN_ID)
        with pg_hook.get_conn() as conn:
            with conn.cursor() as cur:
                print(f"Iniciando o carregamento de {len(dados)} registros no PostgreSQL.")
                for item in dados:
                    # ... (lógica de extração e limpeza dos dados)
                    card, url, endereco, tipo = item.get("card"), item.get("url"), item.get("endereco"), item.get("tipo_imovel")
                    carac = item.get("caracteristicas", {})
                    aluguel, condominio, iptu, total = limpar(carac.get("Aluguel")), limpar(carac.get("Condomínio*")), limpar(carac.get("IPTU*")), limpar(carac.get("TOTAL:"))

                    cur.execute("""
                        INSERT INTO imoveis (card, url, endereco, tipo_imovel, aluguel, condominio, iptu, total, last_updated)
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, CURRENT_TIMESTAMP)
                        ON CONFLICT (card) DO UPDATE SET
                            url = EXCLUDED.url,
                            endereco = EXCLUDED.endereco,
                            tipo_imovel = EXCLUDED.tipo_imovel,
                            aluguel = EXCLUDED.aluguel,
                            condominio = EXCLUDED.condominio,
                            iptu = EXCLUDED.iptu,
                            total = EXCLUDED.total,
                            last_updated = CURRENT_TIMESTAMP;
                    """, (card, url, endereco, tipo, aluguel, condominio, iptu, total))
                print("✅ Dados carregados no PostgreSQL com sucesso.")

    # Define a ordem de execução das tarefas
    create_imoveis_table >> run_load()

# Instancia a DAG
imoveis_etl_dag()
