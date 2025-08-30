import json
import os
import re
import urllib.parse
from airflow.decorators import dag
from datetime import datetime

def normalizar_endereco(endereco):
    endereco = re.sub(r'\bR\b\.?', 'Rua', endereco, flags=re.IGNORECASE)
    endereco = re.sub(r'\bAv\b\.?', 'Avenida', endereco, flags=re.IGNORECASE)
    endereco = re.sub(r'\bPc\b\.?', 'Praça', endereco, flags=re.IGNORECASE)
    return endereco.strip()

def extrair_tipo_imovel(url):
    match = re.search(r'aluguel-([^/]+)', url, re.IGNORECASE)
    if match:
        tipo = match.group(1).split('-')[0]
        tipo = urllib.parse.unquote(tipo).lower()
        if tipo == "prédio":
            return "predio"
        if tipo == "pavilhão":
            return "pavilhao"
        return tipo.capitalize()
    return "Desconhecido"

def limpar_chaves_total(caracteristicas):
    total_keys = [key for key in caracteristicas.keys() if key.strip().startswith("TOTAL")]
    if len(total_keys) > 1:
        preferida = next((k for k in total_keys if k.strip() == "TOTAL:"), total_keys[0])
        novas_caracteristicas = {}
        for k, v in caracteristicas.items():
            if k in total_keys and k != preferida:
                continue
            novas_caracteristicas[k] = v
        return novas_caracteristicas
    return caracteristicas

@dag(
    dag_id="transform_casarao_imoveis_data",
    start_date=datetime(2023, 1, 1),
    schedule=None,
    catchup=False,
    tags=["data_transformation", "imoveis"]
)
def run_transform():
    AIRFLOW_HOME = os.getenv("AIRFLOW_HOME", "/usr/local/airflow")
    RAW_PATH = os.path.join(AIRFLOW_HOME, "include", "data", "resultados_raw.json")
    CLEAN_PATH = "data/resultados_clean.json"

    os.makedirs(os.path.dirname(CLEAN_PATH), exist_ok=True)

    with open(RAW_PATH, "r", encoding="utf-8") as f:
        dados = json.load(f)

    for item in dados:
        item["endereco"] = normalizar_endereco(item["endereco"])
        item["tipo_imovel"] = extrair_tipo_imovel(item["url"])
        item["caracteristicas"] = limpar_chaves_total(item["caracteristicas"])

    with open(CLEAN_PATH, "w", encoding="utf-8") as f:
        json.dump(dados, f, indent=2, ensure_ascii=False)

    print("✅ Dados transformados com sucesso.")

# if __name__ == "__main__":
#     run_transform()

run_transform() # Instancia a DAG