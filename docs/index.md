# Web Scraping - Aluguéis de imóveis

Este projeto realiza web scraping no site [Casarão Imóveis](https://casaraoimoveis.com.br/imoveis/alugueis/pelotas/todos-os-tipos/), com o objetivo de coletar informações de imóveis para aluguel em Pelotas/RS.

A coleta é feita utilizando o Selenium, com rolagem dinâmica da página e abertura individual de cada card de imóvel. Os dados são então transformados e salvos no formato JSON, e então carregados em banco de dados postgres.

Observação: A escolha do site deu-se a dificuldade encontradas, desde scroll infinito a abertura de varias abas para a coleta das informações
## Estrutura da Documentação

1. [Ambiente e Execução](1_setup.md)
2. [Fonte de Dados](2_data_sources.md)
3. [Lógica de Coleta](3_scraping_logic.md)
4. [Orquestração - Airflow](4_airflow.md)
5. [Boas praticas](5_boas_praticas.md)