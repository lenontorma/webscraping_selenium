import json
import psycopg2

def limpar(valor):
    """Remove R$ e converte para float. Retorna None se for inválido."""
    if valor in (None, "---"):
        return None
    valor = valor.replace("R$", "").replace(".", "").replace(",", ".").strip()
    return float(valor)

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
            ON CONFLICT (card) DO NOTHING
        """, (card, url, endereco, tipo, aluguel, condominio, iptu, total))

    conn.commit()
    cur.close()
    conn.close()
    print("✅ Dados carregados no PostgreSQL com sucesso.")

if __name__ == "__main__":
    run_load()
