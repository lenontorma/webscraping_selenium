# Web Scraping - Aluguéis de imóveis

Este projeto realiza web scraping no site [Casarão Imóveis](https://casaraoimoveis.com.br/imoveis/alugueis/pelotas/todos-os-tipos/), com o objetivo de coletar informações de imóveis para aluguel em Pelotas/RS.

A coleta é feita utilizando o Selenium, com rolagem dinâmica da página e abertura individual de cada card de imóvel. Os dados são então transformados e salvos no formato JSON.

Observação: o resultado não gera valor algum, projeto realizado para estudo devido às dificuldades de raspagem encontradas no site, e para a pratica das tecnologias utilizadas.
## Estrutura da Documentação

1. [Fontes de Dados](1_data_sources.md)
2. [Arquitetura do Projeto](2_architecture.md)
3. [Lógica de Coleta](3_scraping_logic.md)
4. [Armazenamento de Dados](4_data_storage.md)
5. [Ambiente e Execução](5_setup.md)