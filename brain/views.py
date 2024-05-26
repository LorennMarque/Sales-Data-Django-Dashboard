from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect
from brain.models import Sale
import csv
import pandas as pd
import matplotlib.pyplot as plt
import io
import base64
import time
import json

data = pd.read_csv("data/supermarket_sales.csv")

df = data
# Group data
df['Order Date'] = pd.to_datetime(df['Order Date'], format='%d/%m/%Y')

df['day'] = df['Order Date'].dt.day
df['month'] = df['Order Date'].dt.month
df['year'] = df['Order Date'].dt.year


def visualize_data(request):
    with open("data/supermarket_sales.csv", "r", encoding="UTF-8") as f:
        data = csv.reader(f)
        sales = []  # List to hold Sale objects
        row_count = 0  # Counter for the rows

        for row in data:
            # 1. Check if the first row is a header
            is_header = row[0] == "Row ID"

            if not is_header:
                created = Sale(
                    row_id=row[0],
                    order_id=row[1],
                    order_date=row[2],
                    ship_date=row[3],
                    ship_mode=row[4],
                    customer_id=row[5],
                    customer_name=row[6],
                    segment=row[7],
                    country=row[8],
                    city=row[9],
                    state=row[10],
                    postal_code=row[11],
                    region=row[12],
                    product_id=row[13],
                    category=row[14],
                    sub_category=row[15],
                    product_name=row[16],
                    sales=row[17]
                )
                # Add the created sale to the list
                sales.append(created)
                row_count += 1

                # Stop if we have reached 200 rows
                if row_count >= 200:
                    break

    context = {
        "sales": sales
    }

    return render(request, 'visualize_data.html', context)

def data_describe(request):
    data = pd.read_csv("data/supermarket_sales.csv")
    descriptions = data['Sales'].describe()
    
    # Definir nombres de cuartiles
    quartile_names = {
        "25%": "q1",
        "50%": "mediana",
        "75%": "q3"
    }
    
    # Reemplazar los nombres de los cuartiles en el índice del DataFrame
    descriptions.index = descriptions.index.map(lambda x: quartile_names.get(x, x))
    
    print(descriptions)
    
    context = {
        "descriptions": descriptions
    }

    return render(request, 'descriptions.html', context)

def render_chart(request):
    data = df.groupby('year')['Sales'].agg('sum').reset_index()  # Reset index to make 'year' a column
    
    # Convert data to JSON
    data_json = data.to_json(orient='records')

    # Render the chart
    context = {
        "data_json": data_json
    }

    return render(request, 'charts.html', context)
