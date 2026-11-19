import sqlite3
import pandas as pd

conexao = sqlite3.connect('olist.db')

# Consulta 1: Qual o status dos pedidos na plataforma?
query_status = """
SELECT 
    order_status AS status,
    COUNT(*) AS total_pedidos
FROM pedidos
GROUP BY order_status
ORDER BY total_pedidos DESC;
"""

# Consulta 2: Pedidos entregues com atraso têm nota de avaliação menor?
query_atraso_nota = """
SELECT 
    CASE 
        WHEN p.order_delivered_customer_date > p.order_estimated_delivery_date THEN 'Atrasado'
        ELSE 'No Prazo'
    END AS status_entrega,
    COUNT(p.order_id) AS qtd_pedidos,
    ROUND(AVG(a.review_score), 2) AS media_nota
FROM pedidos p
JOIN avaliacoes a ON p.order_id = a.order_id
WHERE p.order_status = 'delivered' 
  AND p.order_delivered_customer_date IS NOT NULL
GROUP BY status_entrega;
"""

print("--- STATUS DOS PEDIDOS ---")
print(pd.read_sql_query(query_status, conexao))

print("\n--- IMPACTO DO ATRASO NA NOTA ---")
print(pd.read_sql_query(query_atraso_nota, conexao))

conexao.close()
