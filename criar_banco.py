import sqlite3
import pandas as pd

# 1. Conecta (ou cria) o banco de dados SQLite
conexao = sqlite3.connect('olist.db')

# 2. Lista os arquivos que você baixou e os nomes que as tabelas terão no SQL
arquivos = {
    'pedidos': 'dados/olist_orders_dataset.csv',
    'itens': 'dados/olist_order_items_dataset.csv',
    'avaliacoes': 'dados/olist_order_reviews_dataset.csv'
}

# 3. Lê cada CSV e salva como uma tabela no banco de dados
for nome_tabela, caminho_csv in arquivos.items():
    print(f"Carregando {nome_tabela}...")
    df = pd.read_csv(caminho_csv)
    df.to_sql(nome_tabela, conexao, if_exists='replace', index=False)

print("Banco de dados 'olist.db' criado com sucesso!")
conexao.close()
