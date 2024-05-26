from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect
from brain.models import Sale
import csv
import pandas as pd
import matplotlib.pyplot as plt
import io
import base64

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
    # data = pd.read_csv("data/supermarket_sales.csv")
    # data_avg = data.groupby("Order Date")["Sales"]

    # plt.figure(figsize=(20, 6))
    # data_avg.plot(kind="bar", color="darkblue")
    # plt.ylabel("Sales")
    # plt.xlabel("Date")
    # plt.title("Ventas")
    # plt.xticks(rotation=45, ha="right")
    # plt.tight_layout()
    # # plt.show()

    # my_stringIObytes = io.BytesIO()
    # plt.savefig(my_stringIObytes, format='jpg')
    # my_stringIObytes.seek(0)
    # chart_img = base64.b64encode(my_stringIObytes.read()).decode()

    fig, ax = plt.subplots()
    ax.plot([1,2,3,4], [1,4,2,3])

    # Save the chart to a BytesIO object
    my_stringIObytes = io.BytesIO()
    plt.savefig(my_stringIObytes, format='jpg')
    my_stringIObytes.seek(0)

    # Convert the chart image to base64
    chart_img = base64.b64encode(my_stringIObytes.getvalue()).decode()
    my_stringIObytes.close()  # Close the BytesIO object to free up memory

    context = {
        "chart": chart_img
    }

    # data.drop(data[data["Sales"] < 0].index, inplace=True)
    return render(request, 'charts.html', context)

