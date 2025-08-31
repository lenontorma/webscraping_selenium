# 🏠 Web Scraping - Aluguéis de imóveis

Projeto de web scraping com Python para coletar, transformar e armazenar dados de imóveis para aluguel em Pelotas, RS, disponíveis no site [Casarão Imóveis](https://www.casaraoimoveis.com.br/).

## 🎯 Objetivos e Funcionalidades

O objetivo principal deste projeto é construir um pipeline de dados robusto para a extração automatizada de informações imobiliárias, superando desafios técnicos comuns em web scraping.

As funcionalidades implementadas incluem:

* **Pipeline ETL Completo:** Implementação de um processo de engenharia de dados de ponta a ponta:
    * **Extração (Extract):** Coleta de dados brutos do site Casarão Imóveis utilizando Selenium para lidar com navegação dinâmica e grande volume de dados.
    * **Transformação (Transform):** Limpeza, normalização, estruturação e enriquecimento dos dados coletados para garantir consistência e qualidade.
    * **Carga (Load):** Armazenamento dos dados transformados em um banco de dados PostgreSQL, prontos para consumo e análise.

* **Navegação Dinâmica:** Tratamento de **rolagem infinita** (`infinite scroll`) para garantir o carregamento de todos os imóveis.
* **Coleta Detalhada:** Lógica para abrir **cada imóvel em uma nova aba** e extrair informações específicas.
* **Filtro Inteligente:** Capacidade de diferenciar e ignorar cards de **propaganda** ou elementos não-clicáveis durante a coleta.
* **Documentação Profissional:** Criação de uma documentação completa utilizando **MkDocs**.

## 🛠️ Tecnologias Utilizadas

Este projeto foi construído utilizando as seguintes tecnologias e ferramentas:

![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Selenium](https://img.shields.io/badge/Selenium-43B02A?style=for-the-badge&logo=selenium&logoColor=white)
![Apache Airflow](https://img.shields.io/badge/Apache_Airflow-017CEE?style=for-the-badge&logo=apache-airflow&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-4169E1?style=for-the-badge&logo=postgresql&logoColor=white)
![MkDocs](https://img.shields.io/badge/MkDocs-4A74A5?style=for-the-badge&logo=markdown&logoColor=white)

## 🚀 Como Executar (Quick Start)

Siga os passos abaixo para executar o projeto em seu ambiente local.

### Pré-requisitos

* [Git](https://git-scm.com/)
* [Docker](https://www.docker.com/products/docker-desktop/)
* [Astro CLI](https://docs.astronomer.io/astro/cli/install-cli) (ferramenta para rodar o Airflow localmente)

### Passo a passo

1.  **Clone o repositório:**
    ```bash
    git clone [https://github.com/lenontorma/webscraping_selenium.git](https://github.com/lenontorma/webscraping_selenium.git)
    cd webscraping_selenium
    ```

2.  **Crie o arquivo de ambiente:**
    ```bash
    cp .env.example .env
    ```
    > **Nota:** Os valores padrão neste arquivo já são suficientes para a primeira execução.

3.  **Inicie o ambiente Airflow:**
    ```bash
    astro dev start
    ```

4.  **Acesse e ative a DAG:**
    * Abra a interface do Airflow em [http://localhost:8080](http://localhost:8080).
    * Faça login com usuário `airflow` e senha `airflow`.
    * Na lista de DAGs, encontre a que pertence a este projeto, ative-a no botão de toggle e inicie a primeira execução manualmente.