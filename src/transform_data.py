import json
import os
import re
import urllib.parse

def normalizar_endereco(endereco):
    endereco = re.sub(r'\bR\b\.?', 'Rua', endereco, flags=re.IGNORECASE)
    endereco = re.sub(r'\bAv\b\.?', 'Avenida', endereco, flags=re.IGNORECASE)
    endereco = re.sub(r'\bPc\b\.?', 'Praça', endereco, flags=re.IGNORECASE)
    return endereco.strip()

def extrair_tipo_imovel(url):
    # Extrai tudo após "aluguel-" até a próxima barra (/)
    match = re.search(r'aluguel-([^/]+)', url, re.IGNORECASE)
    if match:
        tipo = match.group(1).split('-')[0]  # Pega apenas a primeira parte (antes de hífens)
        tipo = urllib.parse.unquote(tipo).lower()  # decodifica %c3 etc e coloca minúsculo

        # Normalizações específicas
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

def run_transform():
    RAW_PATH = "data/resultados_raw.json"
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

if __name__ == "__main__":
    run_transform()
