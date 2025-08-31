# Setup e Execução do Projeto

Este documento fornece um guia detalhado para configurar o ambiente de desenvolvimento e executar o pipeline de web scraping localmente.

## 1. Pré-requisitos

Antes de iniciar, é crucial garantir que as seguintes ferramentas estejam instaladas e configuradas corretamente em sua máquina:

* **[Git](https://git-scm.com/)**: Necessário para clonar o repositório e gerenciar o versionamento do código.
* **[Docker Desktop](https://www.docker.com/products/docker-desktop/)**: A plataforma de containerização usada para executar o Apache Airflow e o banco de dados PostgreSQL de forma isolada e consistente.
* **[Astro CLI](https://docs.astronomer.io/astro/cli/install-cli)**: A ferramenta de linha de comando oficial da Astronomer, utilizada para gerenciar o ciclo de vida do ambiente Airflow local (`astro dev start`, `stop`, etc.).

## 2. Configuração do Ambiente Local

Siga os passos abaixo para preparar o projeto após a instalação dos pré-requisitos.

### Passo 1: Clonar o Repositório

Abra um terminal, navegue até o diretório onde deseja salvar o projeto e execute os seguintes comandos:

```bash
git clone [https://github.com/lenontorma/webscraping_selenium.git](https://github.com/lenontorma/webscraping_selenium.git)
cd webscraping_selenium
```

### Passo 2: Configurar Variáveis de Ambiente

O projeto utiliza um arquivo `.env` para gerenciar as credenciais do banco de dados e outras configurações do Airflow.

1.  Crie o seu arquivo `.env` local a partir do template fornecido no repositório:
    ```bash
    cp .env.example .env
    ```

2.  **Análise do Arquivo `.env`**:
    * O arquivo `.env.example` já contém todos os valores padrão necessários para a primeira execução do projeto em um ambiente local.
    * Não é necessário editar o arquivo `.env` para o primeiro `start`. No entanto, se precisar se conectar a um banco de dados externo ou alterar portas, este é o arquivo que você deve modificar.

    Não versione o arquivo "`.env`"
    O arquivo `.env` contém informações sensíveis e está listado no `.gitignore` para prevenir que seja enviado acidentalmente para o repositório remoto. Nunca remova esta linha do `.gitignore`.

## 3. Executando o Pipeline

Com o ambiente configurado, o próximo passo é iniciar os serviços.

1.  A partir da raiz do projeto, execute o comando abaixo:
    ```bash
    astro dev start
    ```

2.  **O que este comando faz?**
    * Ele lê o seu arquivo `docker-compose.yml`.
    * Constrói as imagens Docker necessárias para o Airflow (webserver, scheduler, triggerer) e para o banco de dados PostgreSQL.
    * Inicia todos os contêineres em background (`-d` flag implícita).

## 4. Verificação e Primeiro Uso

Após a execução bem-sucedida do `astro dev start`, o ambiente Airflow estará disponível.

1.  **Acesse a Interface Web:**
    Abra seu navegador e acesse [http://localhost:8080](http://localhost:8080).

2.  **Faça o Login:**
    Utilize as credenciais padrão para o ambiente de desenvolvimento:
    * **Usuário:** `airflow`
    * **Senha:** `airflow`

3.  **Ative e Execute a DAG:**
    * Na página principal, você verá a lista de DAGs disponíveis.
    * Encontre a DAG relacionada a este projeto (ex: `casarao_imoveis_etl`).
    * Ative a DAG utilizando o botão de toggle na coluna "Ativada".
    * Para iniciar a primeira coleta de dados, clique no botão "Play" (▶️) na coluna "Ações".