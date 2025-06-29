# 5. Setup do Projeto

Este guia mostra como configurar o ambiente com **Poetry**, instalar as dependências e executar a pipeline completa — da extração dos dados ao carregamento no PostgreSQL.

---

## 🧱 Requisitos

- [Python](https://www.python.org/) 3.9+
- [Poetry](https://python-poetry.org/)
- [Google Chrome](https://www.google.com/chrome/)
- [ChromeDriver](https://sites.google.com/chromium.org/driver/)
- [PostgreSQL](https://www.postgresql.org/)

---

## ⚙️ Instalação com Poetry

```bash
# 1. Clone o repositório
git clone https://github.com/lenontorma/webscraping_selenium.git
cd webscraping_selenium

# 2. Instale as dependências com Poetry que estão no pyproject.toml
poetry install

# 3. Ative o ambiente virtual do Poetry
poetry shell (Deve ser instalada a extensão "poetry self add poetry-plugin-shell")
```

### 🛠️ Banco PostgreSQL

```bash
CREATE DATABASE webscraping;

\c webscraping

CREATE TABLE imoveis (
    id SERIAL PRIMARY KEY,
    url TEXT,
    endereco TEXT,
    aluguel TEXT,
    condominio TEXT,
    iptu TEXT,
    total TEXT
);

E não se esqueça, ajuste a conexão no load_data.py com suas credenciais PostgreSQL.
```

## 📚 Rodar a Documentação Local
```bash
poetry add mkdocs --group docs
poetry run mkdocs serve
```

Acesse via: http://localhost:8000