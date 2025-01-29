# Meltano ELT Pipeline

Este projeto utiliza o Meltano para executar pipelines de ELT (Extract, Load).

## Pré-requisitos

- Python 3.8 ou superior
- pip (gerenciador de pacotes Python)
- Docker (opcional, para containerização)

## Instalação

1. Clone o repositório:

    ```bash
    git clone https://github.com/eduardoAssuncao/meltano_etl.git
    cd meltano
    ```

2. Crie um ambiente virtual Python:

    ```bash
    python -m venv .venv
    ```

3. Ative o ambiente virtual:

    - **Windows**:
    
    ```bash
    .venv\Scripts\activate
    ```

4. Instale o Meltano:

    ```bash
    pip install meltano
    ```

5. Instale as dependências do projeto:

    ```bash
    meltano install
    ```

6. Verifique todos os lockers do meltano:
    ```bash
    meltano lock --update
    ```

7. Entre na pasta do meltano_etl:
    ```bash
    cd meltano_etl
    ```
7. Crie dois containers do postgres (sorcedb e targetdb):
    ```bash
    docker run -d --name sourcedb -p 5000:5432 -e POSTGRES_USER=meuuser -e POSTGRES_PASSWORD=minhasenha -e POSTGRES_DB=sourcedb postgres
    docker run -d --name targetdb -p 5001:5432 -e POSTGRES_USER=meuuser -e POSTGRES_PASSWORD=minhasenha -e POSTGRES_DB=targetdb postgres
    ```
8. Faça a conexão a cada um dos bancos usando o dbeaver e execute a ddl de criação das tabelas no sourcedb:
    local do dump: ./meltano_etl/data/northwind.sql

9. Execute o processo de extração e load:
    ```bash
    ./execution_meltano.bash
    ```

10. Faça o select no banco targetdb:
    SELECT * FROM categories;
    SELECT * FROM customers;
    SELECT * FROM employees;
    SELECT * FROM employee_territories;
    SELECT * FROM orders;
    SELECT * FROM products;
    SELECT * FROM region;
    SELECT * FROM shippers;
    SELECT * FROM suppliers;
    SELECT * FROM territories;
    SELECT * FROM us_states;
