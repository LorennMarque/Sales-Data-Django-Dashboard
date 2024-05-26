import pandas as pd
import matplotlib.pyplot as plt

data=pd.read_csv("data/supermarket_sales.csv")


ventas_por_categoria = data.groupby('Category')['Sales'].sum()

plt.figure(figsize=(10, 6))
ventas_por_categoria.plot(kind='bar')
plt.title('Ventas Totales por Categoría')
plt.xlabel('Categoría')
plt.ylabel('Ventas Totales ($)')
plt.xticks(rotation=45)
plt.grid(True)
plt.show()
