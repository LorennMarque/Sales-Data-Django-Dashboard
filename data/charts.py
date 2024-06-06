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

# ----------------------------------------------------------------------------------
# Los productos más vendidos de cada año con sus nombres
top_10_por_año = df.groupby(['year', 'Product Name'])['Sales'].count().groupby('year').nlargest(3).reset_index(level=0, drop=True)
print(top_10_por_año)

# ----------------------------------------------------------------------------------

# Ingresos x mes y año
# sales_per_year = df.groupby(['year','month'])['Sales'].agg('sum').reset_index()  
# print(sales_per_year)

# ----------------------------------------------------------------------------------

# Cantidad de ventas x mes y año
# amount_of_sales_per_month_and_year = df.groupby(['year','month'])['Sales'].agg('count').reset_index()  
# print(amount_of_sales_per_month_and_year)

# ----------------------------------------------------------------------------------

# TOP 10 clientes que más han gastado
# print(df.groupby('Customer Name')['Sales'].agg('sum').nlargest(10).reset_index())

# ----------------------------------------------------------------------------------

# Sectores Segments con mayores revenues
# print(df.groupby('Segment')['Sales'].agg("sum").reset_index())

# ----------------------------------------------------------------------------------

# TOP 5 productos que más ganancias dieron (piechart)
# print(df.groupby('Product Name')['Sales'].agg("sum").nlargest(5).reset_index())

# ----------------------------------------------------------------------------------

# Promedio de gasto por cliente por año
# avg_sales_per_year = df.groupby('year')['Sales'].mean().reset_index()
# print(avg_sales_per_year)

# ----------------------------------------------------------------------------------

# year_of_interest = 2017  # Cambia este valor al año que te interese

# df_year_of_interest = df[df['year'] == year_of_interest]

# avg_sales_per_year_of_interest = df_year_of_interest.groupby('month')['Sales'].mean().reset_index()

# print(avg_sales_per_year_of_interest)



# ----------------------------------------------------------------------------------


# print("Cuarto:  Ingresos promedio por cliente")
# print((df.groupby("Customer ID")['Sales'].mean()).reset_index()['Sales'])

# ==================== VISTA GENERAL ==================================
# print("Primero:  monto de ventas en 2017")

# print(df[df['year'] == 2017]['Sales'].sum())
# df[df['year'] == 2017]['Sales'].sum()d

# print("Segundo: cantidad de ventas en 2017")
# print(df[df['year'] == 2017]['Sales'].count())

# print("Tercero: Tiempo promedio de envío (promedio)")
# print(f"Tarda {(df['delivery'].dt.total_seconds() / 3600).mean()} horas.")

# print("Cuarto:  Ingresos promedio por cliente")
# print(round(((df.groupby("Customer ID")['Sales'].sum()).reset_index()['Sales']).mean(),3))

# print("Quinto: Monto de ventas por estado")
# print(df.groupby('State')['Sales'].sum().reset_index().sort_values("Sales",ascending=False))

# print("Productos mas vendidos (como el de best selling products)")
# print(df["Product Name"].value_counts().reset_index())

# ==================== PEDIDOS =====================================

# print("Tiempo promedio de envio por Ship Mode BARCHART")
# print(round(df.groupby('Ship Mode')['delivery'].mean()).reset_index())
# avg_delivery_time_per_ship_mode = round(df.groupby('Ship Mode')['delivery'].mean().dt.total_seconds() / 3600 , 3).reset_index()
# print(avg_delivery_time_per_ship_mode)
# avg_delivery_time_per_ship_mode = avg_delivery_time_per_ship_mode.to_json(orient='records')

# print('avg_delivery_time_per_ship_mode = avg_delivery_time_per_ship_mode.to_json(orient='records')
# print(round(df.groupby(["year","month"])['delivery'].mean().dt.total_seconds() / 3600,3))

# Primero, agrupamos por 'year' y 'month' y calculamos el promedio de 'delivery' en horas
# average_delivery_hours = df.groupby(["year", "month"])['delivery'].mean().dt.total_seconds() / 3600

# Convertimos el resultado a un DataFrame
# average_delivery_hours = average_delivery_hours.reset_index()

# Creamos una nueva columna 'date' en el formato 'mes-año'
# average_delivery_hours['date'] = average_delivery_hours['month'].astype(str) + '-' + average_delivery_hours['year'].astype(str)

# Seleccionamos solo las columnas 'date' y 'delivery'
# result_data = average_delivery_hours[['date', 'delivery']]

# Renombramos la columna 'delivery' a 'average_delivery_hours'
# result_data.columns = ['date', 'average_delivery_hours']

# Redondeamos los valores a 3 decimales
# result_data['average_delivery_hours'] = result_data['average_delivery_hours'].round(3)
# print(result_data)
# print("alguna tabla, con las columnas que sean numero de orden, nombre del cliente, fecha de orden y tiempo de entrega.")

# pedidos_table = df[['Order ID','Customer Name','Order Date','Ship Date','delivery']]
# print(pedidos_table)

# ==================== PRODUCTOS ====================================
# print("grafico de 5 subcategorias mas vendidas ")
# print(df.groupby("Sub-Category")["Sales"].sum().reset_index().sort_values("Sales", ascending=False))

# print("tabla de los productos con nombre del producto , categoría, subcategoría, cantidad de vendidos")
# print(df.groupby(['Product Name','Category','Sub-Category'])['Sales'].count().reset_index().sort_values("Sales",ascending=False))


# ==================== CLIENTES ====================================
# print("grafico de ventas por ciudad")
# print(df.groupby('City')['Sales'].sum().reset_index().sort_values("Sales",ascending=False))

# print("Clientes que más compraros :)")
# print("==========================================")
# print(df.groupby(['Order ID', 'Customer Name'])['Sales'].sum().reset_index().sort_values("Sales",ascending=False))

# print("tabla de clientes con nombre del cliente,  gasto, fecha del ultimo pedido de cada cliente y ciudad") # SALES ES MONTO TOTAL GASTADO4
# tabla_clientes = print(df.groupby(["Customer Name"]).agg(total_sales=("Sales","sum"), last_order =('Order Date', 'max')).reset_index().sort_values("total_sales",ascending = False))   