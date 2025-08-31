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

*Esta seção será adicionada em breve com os comandos essenciais para a execução do projeto.*