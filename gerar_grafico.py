import sqlite3
import pandas as pd
import matplotlib.pyplot as plt

conexao = sqlite3.connect('olist.db')

query_atraso_nota = """
SELECT 
    CASE 
        WHEN p.order_delivered_customer_date > p.order_estimated_delivery_date THEN 'Entrega Atrasada'
        ELSE 'Entrega No Prazo'
    END AS status_entrega,
    ROUND(AVG(a.review_score), 2) AS media_nota
FROM pedidos p
JOIN avaliacoes a ON p.order_id = a.order_id
WHERE p.order_status = 'delivered' 
  AND p.order_delivered_customer_date IS NOT NULL
GROUP BY status_entrega
ORDER BY media_nota DESC;
"""

df = pd.read_sql_query(query_atraso_nota, conexao)
conexao.close()

# Criando o gráfico
plt.figure(figsize=(8, 5))
cores = ['#2E86C1', '#E74C3C']  # Azul para no prazo, vermelho para atrasado
barras = plt.bar(df['status_entrega'], df['media_nota'], color=cores, width=0.5)

# Títulos e rótulos
plt.title('Impacto do Atraso na Satisfação do Cliente (Nota 1 a 5)', fontsize=13, fontweight='bold', pad=15)
plt.ylabel('Nota Média de Avaliação', fontsize=11)
plt.ylim(0, 5.5)

# Removendo bordas desnecessárias para ficar mais moderno
plt.gca().spines['top'].set_visible(False)
plt.gca().spines['right'].set_visible(False)

# Colocando os valores exatos em cima de cada barra
for barra in barras:
    altura = barra.get_height()
    plt.text(barra.get_x() + barra.get_width()/2, altura + 0.15, f'{altura:.2f}', 
             ha='center', va='bottom', fontsize=12, fontweight='bold')

plt.tight_layout()
plt.savefig('impacto_atraso_nota.png', dpi=300)
print("Gráfico 'impacto_atraso_nota.png' salvo com sucesso!")
