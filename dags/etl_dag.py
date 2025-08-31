# dags/etl_dag.py
from airflow.decorators import dag
from datetime import datetime

# Importar apenas as tasks
from dag_scraper import run_extract_task
from dag_transform import run_transform_task
from dag_load import run_load_task

@dag(
    dag_id="casarao_imoveis_etl",
    start_date=datetime(2023, 1, 1),
    schedule=None,
    catchup=False,
    tags=["etl", "web_scraping", "imoveis"]
)
def casarao_imoveis_etl_dag():
    # Chama as tasks (não DAGs)
    extract = run_extract_task()
    transform = run_transform_task()
    load = run_load_task()

    # Encadeia as tasks
    extract >> transform >> load

# Instancia a DAG
casarao_imoveis_etl_dag()
