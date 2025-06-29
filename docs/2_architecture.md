# 2. Arquitetura do Projeto

Este projeto é dividido em duas fases principais: **extração** e **transformação** de dados.

## 🗂️ Estrutura de Diretórios

webscraping_selenium              
├─ data                            
│  ├─ resultados_clean.json       
│  └─ resultados_raw.json         
├─ docs                           
│  ├─ assets                      
│  ├─ 0_index.md                  
│  ├─ 1_data_sources.md           
│  ├─ 2_architecture.md           
│  ├─ 3_scraping_logic.md         
│  ├─ 4_data_storage.md           
│  └─ 5_setup.md                  
├─ sql                            
│  └─ create_table.sql            
├─ src                                  
│  ├─ extract_data.py             
│  ├─ load_data.py                
│  └─ transform_data.py                                     
├─ main.py                        
├─ poetry.lock                    
├─ pyproject.toml                 
└─ README.md                      


## ⚙️ Componentes do Pipeline

### 🟦 1. `extract_data.py`
Responsável por:
- Utilizar o Selenium para navegar pela página principal e abrir os links dos imóveis.
- Extrair o endereço e as características de cada imóvel.
- Salvar o resultado bruto em `data/resultados_raw.json`.

### 🟨 2. `transform_data.py`
Responsável por:
- Normalizar os endereços (ex: "R." → "Rua", "Av." → "Avenida").
- Eliminar entradas duplicadas ou inconsistentes da chave `"TOTAL"`.
- Salvar o resultado limpo em `data/resultados_clean.json`.

### 🟩 3. `load_data.py`
Responsável por:
- Ler o arquivo `resultados_clean.json`.
- Conectar-se a um banco de dados PostgreSQL.
- Inserir os registros na tabela apropriada.

## ⚙️ Pipeline de Execução

```mermaid
flowchart TD
    Start([🚀 Início da Pipeline])

    Extract[📥 extract_data.py<br> ➡️ Coleta dados com Selenium]
    Transform[🧹 transform_data.py<br>➡️ Gera resultados_clean.json]
    Load[🗄️ load_data.py<br>➡️ Insere dados no PostgreSQL]

    DB[(🟢 PostgreSQL<br>Tabela de imóveis)]

    Start --> Extract --> Transform --> Load --> DB
```