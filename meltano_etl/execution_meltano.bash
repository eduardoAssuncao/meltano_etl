#!/bin/bash

# Ativar o ambiente virtual do Meltano (caso esteja usando um)
source .venv/bin/activate 2>/dev/null

echo "Iniciando extração e carga de dados..."

# Executar o extractor do PostgreSQL e carregar para o destino PostgreSQL
echo "Extraindo do PostgreSQL e carregando para o PostgreSQL..."
meltano run tap-postgres target-postgres-csv

# Executar o extractor CSV e carregar para o destino CSV
echo "Extraindo do CSV e carregando para CSV..."
meltano run tap-csv target-csv

# Executar o extractor CSV (dados do PostgreSQL) e carregar para o destino PostgreSQL
echo "Extraindo do CSV gerado pelo PostgreSQL e carregando para o PostgreSQL..."
meltano run tap-csv-postgres target-postgres

# Finalização
echo "Processo concluído!"


