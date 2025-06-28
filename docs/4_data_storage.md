# 4. Armazenamento de Dados

Os dados coletados e transformados passam por duas formas de armazenamento:

1. **Arquivos locais** (`JSON`) para debug e histórico.
2. **Banco de dados PostgreSQL** para análise estruturada e integração com outras ferramentas.

---

## 📁 Armazenamento em Arquivos

Após cada etapa da pipeline, os dados são salvos para inspeção ou reprocessamento:

```mermaid
flowchart TD
    A[📥 extract_data.py] --> B[data/resultados_raw.json]
    B --> C[🧹 transform_data.py]
    C --> D[data/resultados_clean.json]
```

## 🗄️ Armazenamento em Banco de Dados (PostgreSQL)
O script load_data.py é responsável por ler o resultados_clean.json e inserir os dados no banco PostgreSQL.

```mermaid
flowchart TD
    JSON[data/resultados_clean.json] --> LOAD[load_data.py]
    LOAD --> DB[(🟢 PostgreSQL<br>Tabela de imóveis)]
```

## 🧱 Modelo de Tabela
A estrutura no banco é planejada para refletir as informações dos imóveis. Um modelo típico da tabela pode ser:

CREATE TABLE imoveis (
    id SERIAL PRIMARY KEY,
    url TEXT,
    endereco TEXT,
    aluguel TEXT,
    condominio TEXT,
    iptu TEXT,
    total TEXT
);


## ✅ Resultado
```mermaid
flowchart TD
    Inicio([🚀 Dados transformados])
    Inicio --> Arq[📁 Salvo em JSON]
    Arq --> Banco[🗃️ Inserido no PostgreSQL]
    Banco --> Analise[📈 Pronto para análise ou dashboards]
```