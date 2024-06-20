from statsmodels.tsa.statespace.sarimax import SARIMAX
# import matplotlib.pyplot as plt
import pandas as pd

# Cargar datos
data = pd.read_csv("data/supermarket_sales.csv")

df = data
# Group data
df['Order Date'] = pd.to_datetime(df['Order Date'], format='%d/%m/%Y')
# df['Ship Date'] = pd.to_datetime(df['Ship Date'], format='%d/%m/%Y')

df['day'] = df['Order Date'].dt.day
df['month'] = df['Order Date'].dt.month
df['year'] = df['Order Date'].dt.year
# df['delivery'] = df['Ship Date'] - df['Order Date']
df['year_month'] = df['year'].astype(str) + '-' + df['month'].astype(str).str.zfill(2)

clean = df.groupby("year_month")['Sales'].count().reset_index()
# train_data = clean[clean['year_month'] < '2018-01']

# Ajustar el modelo SARIMA a todos los datos disponibles
model = SARIMAX(clean['Sales'], order=(0, 1, 1), seasonal_order=(0, 1, 1, 12))
model_fit = model.fit()

# Hacer predicciones para el año 2019
start_idx = clean.index[-1] + 1  # Índice del primer período después del conjunto de datos conocidos
end_idx = start_idx + 11  # Predicciones para los siguientes 12 meses (todo el año 2019)

predictions = model_fit.predict(start=start_idx, end=end_idx, dynamic=True)

# Guardar valores del eje x y el eje y en listas
x_values = list(predictions.index)
y_values = list(predictions)

# Visualizar las predicciones para el año 2019
# plt.figure(figsize=(10, 6))
# plt.plot(clean.index, clean['Sales'], label='Datos reales')
# plt.plot(predictions.index, predictions, color='red', label='Predicciones')
# plt.title('Predicciones para 2019 (SARIMA)')
# plt.xlabel('Índice')
# plt.ylabel('Ventas')
# plt.legend()
# plt.grid(True)
# plt.show()

# Imprimir las listas de valores de x y y
print("Valores del eje x (índice):", x_values)
print("Valores del eje y (predicciones):", y_values)
