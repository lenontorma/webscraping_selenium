# dags/dag_load.py
import os
import json
from airflow.decorators import dag, task
from datetime import datetime
from airflow.providers.postgres.hooks.postgres import PostgresHook

POSTGRES_CONN_ID = "postgres_default"

# -------------------- TASK --------------------
@task
def run_load_task():
    """
    Carrega os dados limpos do JSON para o PostgreSQL.
    Se a tabela existir, ela será substituída.
    """
    AIRFLOW_HOME = os.getenv("AIRFLOW_HOME", "/usr/local/airflow")
    CLEAN_PATH = os.path.join(AIRFLOW_HOME, "include", "data", "resultados_clean.json")

    # Lê os dados
    with open(CLEAN_PATH, "r", encoding="utf-8") as f:
        dados = json.load(f)

    # Conecta no PostgreSQL
    pg_hook = PostgresHook(postgres_conn_id=POSTGRES_CONN_ID)
    with pg_hook.get_conn() as conn:
        with conn.cursor() as cur:
            # Deleta tabela se existir
            cur.execute("DROP TABLE IF EXISTS imoveis;")
            conn.commit()

            # Cria a tabela
            cur.execute("""
                CREATE TABLE imoveis (
                    card VARCHAR(255) PRIMARY KEY,
                    url TEXT,
                    endereco TEXT,
                    tipo_imovel VARCHAR(255),
                    aluguel NUMERIC(10,2),
                    condominio NUMERIC(10,2),
                    iptu NUMERIC(10,2),
                    total NUMERIC(10,2),
                    last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                );
            """)
            conn.commit()

            # Insere os dados
            for item in dados:
                card, url, endereco, tipo = item.get("card"), item.get("url"), item.get("endereco"), item.get("tipo_imovel")
                carac = item.get("caracteristicas", {})

                def limpar(valor):
                    if valor in (None, "---"): return None
                    valor = str(valor).replace("R$", "").replace("\xa0", " ").replace(".", "").replace(",", ".").strip()
                    try:
                        return float(valor)
                    except (ValueError, TypeError):
                        return None

                aluguel = limpar(carac.get("Aluguel"))
                condominio = limpar(carac.get("Condomínio*"))
                iptu = limpar(carac.get("IPTU*"))
                total = limpar(carac.get("TOTAL:"))

                cur.execute("""
                    INSERT INTO imoveis (card, url, endereco, tipo_imovel, aluguel, condominio, iptu, total, last_updated)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, CURRENT_TIMESTAMP);
                """, (card, url, endereco, tipo, aluguel, condominio, iptu, total))
            conn.commit()

    print(f"✅ {len(dados)} registros carregados no PostgreSQL com sucesso.")

# -------------------- DAG --------------------
@dag(
    dag_id="load_casarao_imoveis_data",
    start_date=datetime(2023, 1, 1),
    schedule=None,
    catchup=False,
    tags=["load", "imoveis"]
)
def load_dag():
    run_load_task()

# Instancia a DAG
load_dag()
