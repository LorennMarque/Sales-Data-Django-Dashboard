import pandas as pd
import datetime

# Leer el archivo CSV
data = pd.read_csv("data/supermarket_sales.csv")

# año y ganancias

df = data

df['Order Date'] = pd.to_datetime(df['Order Date'], format='%d/%m/%Y')

df['day'] = df['Order Date'].dt.day
df['month'] = df['Order Date'].dt.month
df['year'] = df['Order Date'].dt.year

# print(df.groupby('year')['Sales'].agg('sum')) # MUY IMPORTANTE
data = df.groupby('year')['Sales'].agg('sum') # MUY IMPORTANTE
print(pd.DataFrame(data))
