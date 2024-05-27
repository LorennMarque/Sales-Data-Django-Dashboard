import pandas as pd
data = pd.read_csv("data/supermarket_sales.csv")

df = data
# Group data
df['Order Date'] = pd.to_datetime(df['Order Date'], format='%d/%m/%Y')

df['day'] = df['Order Date'].dt.day
df['month'] = df['Order Date'].dt.month
df['year'] = df['Order Date'].dt.year

print(df['Customer Name'].value_counts().reset_index())

