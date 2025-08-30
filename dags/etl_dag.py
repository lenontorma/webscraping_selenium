from airflow.decorators import dag, task
from datetime import datetime

# Importar as funções DAG de cada arquivo
from dag_scraper import run_extract
from dag_transform import run_transform
from dag_load import run_load

@dag(
    dag_id="casarao_imoveis_etl",
    start_date=datetime(2023, 1, 1),
    schedule=None,
    catchup=False,
    tags=["etl", "web_scraping", "imoveis"]
)
def casarao_imoveis_etl_dag():
    # Definir as tarefas chamando as funções DAG importadas
    extract_task = run_extract()
    transform_task = run_transform()
    load_task = run_load()

    # Definir as dependências das tarefas
    extract_task >> transform_task >> load_task

# Instanciar a DAG para que o Airflow a detecte
casarao_imoveis_etl_dag()
