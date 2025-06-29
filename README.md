# 🏠 Web Scraping - Aluguéis de imóveis

Projeto de **web scraping com Python** para coletar, transformar e armazenar dados de imóveis para aluguel em Pelotas, RS, disponíveis no site [Casarão Imóveis](https://casaraoimoveis.com.br/).

---

## 🔧 Tecnologias Utilizadas

| Ferramenta        | Descrição                              |
|-------------------|------------------------------------------|
| ![Python](https://img.shields.io/badge/Python-3.9+-blue?logo=python) | Linguagem principal do projeto |
| ![Selenium](https://img.shields.io/badge/Selenium-Automação-43B02A?logo=selenium) | Automação e scraping da web |
| ![Poetry](https://img.shields.io/badge/Poetry-Gerenciador%20de%20pacotes-1C1C1C?logo=python) | Gerenciamento de dependências e ambiente |
| ![MkDocs](https://img.shields.io/badge/MkDocs-Documentação-009688?logo=readthedocs) | Geração de documentação estática |
| ![PostgreSQL](https://img.shields.io/badge/PostgreSQL-Banco%20de%20dados-336791?logo=postgresql) | Armazenamento estruturado dos dados |

---

## 🔍 Objetivo

> Este projeto foi desenvolvido com **finalidade de estudo prático** em web scraping, automação e engenharia de dados.

O site da [Casarão Imóveis](https://casaraoimoveis.com.br/) foi escolhido propositalmente devido aos **desafios técnicos envolvidos no scraping**, incluindo:

- Rolagem infinita para carregar todos os imóveis
- Presença de cards que são **propagandas ou não clicáveis**
- Necessidade de abrir **cada imóvel em uma nova aba** para coletar dados detalhados
- Mais de 1000 imoveis para serem coletados

Além disso, o projeto permitiu exercitar o uso de:
- Coleta automatizada com Selenium
- Estruturação do pipeline em etapas: extração, transformação e carga (ETL)
- Armazenamento dos dados em PostgreSQL
- Documentação profissional com MkDocs + Mermaid

---

## 🧠 Arquitetura (ETL)

```mermaid
flowchart TD
    A[📥 extract_data.py<br>➡️ Scraping com Selenium] --> B[🧹 transform_data.py<br>➡️ Limpeza e normalização]
    B --> C[🗄️ load_data.py<br>➡️ Inserção no PostgreSQL]
```

## 🚀 Como Executar o Projeto

Pré-requisitos

 - Python 3.9+

 - Google Chrome + ChromeDriver compatível

 - PostgreSQL (opcional)

 - Poetry


## Instalação
```bash
# 1. Clone o projeto
git clone https://github.com/seu-usuario/webscraping_selenium.git
cd webscraping_selenium

# 2. Instale as dependências
poetry install

# 3. Ative o ambiente virtual
poetry shell (Deve ser instalada a extensão "poetry self add poetry-plugin-shell")

# 4. Executar no Postgres

O código do caminho: sql\create_table.sql

```

## Execução da pipeline
```bash
poetry run main.py
```

## Projeto publicado no GitHub Pages:
📎 [Acesse a documentação](https://lenontorma.github.io/webscraping_selenium/)