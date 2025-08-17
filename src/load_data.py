import json
import psycopg2

def limpar(valor):
    if valor in (None, "---"):
        return None
    valor = str(valor).replace("R$", "").replace("\xa0", " ").replace(".", "").replace(",", ".").strip()
    try:
        return float(valor)
    except ValueError:
        return None

def run_load():
    with open("data/resultados_clean.json", "r", encoding="utf-8") as f:
        dados = json.load(f)

    with open("credentials.json", "r") as f:
        cred = json.load(f)

    conn = psycopg2.connect(
        dbname=cred["dbname"],
        user=cred["user"],
        password=cred["password"],
        host=cred["host"]
    )
    cur = conn.cursor()

    for item in dados:
        card = item.get("card")
        url = item.get("url")
        endereco = item.get("endereco")
        tipo = item.get("tipo_imovel")
        carac = item.get("caracteristicas", {})

        aluguel = limpar(carac.get("Aluguel"))
        condominio = limpar(carac.get("Condomínio*"))
        iptu = limpar(carac.get("IPTU*"))
        total = limpar(carac.get("TOTAL:"))

        cur.execute("""
            INSERT INTO imoveis (card, url, endereco, tipo_imovel, aluguel, condominio, iptu, total)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            ON CONFLICT (card) DO UPDATE SET
                url = EXCLUDED.url,
                endereco = EXCLUDED.endereco,
                tipo_imovel = EXCLUDED.tipo_imovel,
                aluguel = EXCLUDED.aluguel,
                condominio = EXCLUDED.condominio,
                iptu = EXCLUDED.iptu,
                total = EXCLUDED.total
        """, (card, url, endereco, tipo, aluguel, condominio, iptu, total))

    conn.commit()
    cur.close()
    conn.close()
    print("✅ Dados carregados no PostgreSQL com sucesso.")

if __name__ == "__main__":
    run_load()
