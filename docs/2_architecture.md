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


## ⚙️ Componentes principais

### 1. `extract.py`
Responsável por:
- Iniciar o navegador com Selenium.
- Fazer scroll na página principal para carregar todos os imóveis.
- Navegar até a página individual de cada imóvel.
- Extrair o endereço e as características.
- Exportar os dados brutos para `data/resultados_raw.json`.

### 2. `transform.py`
Responsável por:
- Corrigir abreviações em endereços (ex: "R." → "Rua").
- Remover duplicatas da chave `"TOTAL"` no dicionário de características.
- Exportar os dados limpos para `data/resultados_clean.json`.

## 🔁 Fluxo de Execução

```mermaid
graph TD
    A[extract.py] -->|Salva JSON bruto| B[resultados_raw.json]
    B --> C[transform.py]
    C -->|Salva JSON limpo| D[resultados_clean.json]
