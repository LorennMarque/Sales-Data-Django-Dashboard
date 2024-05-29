import pandas as pd
data = pd.read_csv("data/supermarket_sales.csv")

df = data
# Group data
df['Order Date'] = pd.to_datetime(df['Order Date'], format='%d/%m/%Y')
df['Ship Date'] = pd.to_datetime(df['Ship Date'], format='%d/%m/%Y')

df['day'] = df['Order Date'].dt.day
df['month'] = df['Order Date'].dt.month
df['year'] = df['Order Date'].dt.year
df['delivery'] = df['Ship Date'] - df['Order Date']

# print("Cuarto:  Ingresos promedio por cliente")
# print((df.groupby("Customer ID")['Sales'].mean()).reset_index()['Sales'])
# ==================== VISTA GENERAL ====================================
# print("Primero:  monto de ventas en 2017")
# print(df[df['year'] == 2017]['Sales'].sum())

# print("Segundo: cantidad de ventas en 2017")
# print(df[df['year'] == 2017]['Sales'].count())

# print("Tercero: Tiempo promedio de envío (promedio)")
# print(f"Tarda {(df['delivery'].dt.total_seconds() / 3600).mean()} horas.")

print("Cuarto:  Ingresos promedio por cliente")
print(round(((df.groupby("Customer ID")['Sales'].sum()).reset_index()['Sales']).mean(),3))

# print("Quinto: Monto de ventas por estado")
# print(df.groupby('State')['Sales'].sum().reset_index().sort_values("Sales",ascending=False))

# print("Productos mas vendidos (como el de best selling products)")
# print(df["Product Name"].value_counts())

# ==================== PEDIDOS =========================================

# print("Tiempo promedio de envio por Ship Mode BARCHART")
# print(round(df.groupby('Ship Mode')['delivery'].mean()))

# print('Tiempo de delivery x mes') 
# print(round(df.groupby(["year","month"])['delivery'].mean().dt.total_seconds() / 3600,3))

# print("alguna tabla, con las columnas que sean numero de orden, nombre del cliente, fecha de orden y tiempo de entrega.")

# pedidos_table = df[['Order ID','Customer Name','Order Date','Ship Date','delivery']]
# print(pedidos_table)

# ==================== PRODUCTOS ======================================
# print("grafico de 5 subcategorias mas vendidas ")
# print(df.groupby("Sub-Category")["Sales"].sum().reset_index().sort_values("Sales", ascending=False))

# print("tabla de los productos con nombre del producto , categoría, subcategoría, cantidad de vendidos")
# print(df.groupby(['Product Name','Category','Sub-Category'])['Sales'].count().reset_index().sort_values("Sales",ascending=False))


# ==================== CLIENTES ======================================
# print("grafico de ventas por ciudad")
# print(df.groupby('City')['Sales'].sum().reset_index().sort_values("Sales",ascending=False))

# print("Clientes que más compraros :)")
# print("=============================================")
# print(df.groupby(['Order ID', 'Customer Name'])['Sales'].sum().reset_index().sort_values("Sales",ascending=False))

# print("tabla de clientes con nombre del cliente,  gasto, fecha del ultimo pedido de cada cliente y ciudad") # SALES ES MONTO TOTAL GASTADO4
# tabla_clientes = print(df.groupby(["Customer Name"]).agg(total_sales=("Sales","sum"), last_order =('Order Date', 'max')).reset_index().sort_values("total_sales",ascending = False))   