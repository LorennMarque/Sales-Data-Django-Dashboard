# Create your views here.
from django.shortcuts import render, redirect
import csv
import pandas as pd
import matplotlib.pyplot as plt
from django.db.models import Sum, Count, Avg
from brain.models import Sale

data = pd.read_csv("data/supermarket_sales.csv")

df = data
# Group data
df['Order Date'] = pd.to_datetime(df['Order Date'], format='%d/%m/%Y')
df['Ship Date'] = pd.to_datetime(df['Ship Date'], format='%d/%m/%Y')

df['day'] = df['Order Date'].dt.day
df['month'] = df['Order Date'].dt.month
df['year'] = df['Order Date'].dt.year
df['delivery'] = df['Ship Date'] - df['Order Date']


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

def panel_principal(request):
    sales_per_year = df.groupby('year')['Sales'].agg('sum').reset_index()  
    sales_per_year = sales_per_year.to_json(orient='records')

    sales_amount_per_year = df['year'].value_counts().reset_index()
    sales_amount_per_year = sales_amount_per_year.to_json(orient='records')

    top_10_sales_per_state = df.groupby("State")["Sales"].agg("sum").reset_index()
    top_10_sales_per_state = top_10_sales_per_state.nlargest(10, 'Sales').reset_index(drop=True)
    top_10_sales_per_state = top_10_sales_per_state.to_json(orient='records')

    top_subcategories = df.groupby("Sub-Category")["Sales"].sum().nlargest(5).reset_index()
    top_subcategories = top_subcategories.to_json(orient='records')

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
                if row_count >= 10:
                    break

    context = {
        "sales_per_year": sales_per_year,
        "sales_amount_per_year": sales_amount_per_year,
        "top_10_sales_per_state":  top_10_sales_per_state, 
        "top_5_subcategories": top_subcategories,
        "sales_table":sales
    }

    return render(request, 'inicio.html', context)


def nav(request):
    context = {
        "sales_per_year": "hola",
    }

    return render(request, 'navegacion.html', context)



# ==================== VISTA GENERAL ====================================
def vista_general(request):

    sales_per_year = df.groupby('year')['Sales'].agg('sum').reset_index()  
    sales_per_year = sales_per_year.to_json(orient='records')

    # 1. Guardar una variable con los datos
    year_sales_total = round(df['Sales'].sum(),2)
    # year_sales_total = df[df['year'] == 2017]['Sales'].sum()
    year_sales_total = f"{int(year_sales_total):,}".replace(",", ".") + "," + str(year_sales_total).split('.')[1]
    year_sales_amount = df[df['year'] == 2017]['Sales'].count()
    
    avg_delivery_time = round((df['delivery'].dt.total_seconds() / 3600).mean(),2)

    avg_income_per_costumer = round(((df.groupby("Customer ID")['Sales'].sum()).reset_index()['Sales']).mean(),2)

    sales_amount_per_state = df.groupby('State')['Sales'].sum().reset_index().sort_values("Sales",ascending=False)
    sales_amount_per_state = sales_amount_per_state.to_json(orient='records')

    best_selling_products = df["Product Name"].value_counts().reset_index()
    best_selling_products = best_selling_products.to_json(orient='records')

    # 3. Enviarla por context
    context = {
        "sales_per_year": sales_per_year,
        "year_sales_total": year_sales_total,
        "year_sales_amount" : year_sales_amount,
        "avg_delivery_time" : avg_delivery_time,
        "avg_income_per_costumer" : avg_income_per_costumer,
        "sales_amount_per_state" : sales_amount_per_state,
        "best_selling_products" : best_selling_products
    }
    return render(request, 'vista_general.html', context)

# def vista_general(request):
#     # Total de ventas en el año 2017
#     year_sales_total = Sale.objects.filter(order_date__year=2017).aggregate(Sum('sales'))['sales__sum'] or 0

#     # Cantidad de ventas en el año 2017
#     year_sales_amount = Sale.objects.filter(order_date__year=2017).count()

#     # Tiempo de entrega promedio en horas
#     avg_delivery_time = Sale.objects.aggregate(avg_delivery=Avg('delivery_time'))['avg_delivery'] or 0

#     # Ingreso promedio por cliente
#     # Suma de las ventas agrupadas por cliente, luego se calcula el promedio de estas sumas
#     avg_income_per_customer = round(Sale.objects.values('customer_id').annotate(total_sales=Sum('sales')).aggregate(Avg('total_sales'))['total_sales__avg'], 3) or 0

#     # Total de ventas por estado
#     # Se agrupan las ventas por estado y se calcula la suma de ventas para cada estado
#     sales_amount_per_state = Sale.objects.values('state').annotate(total_sales=Sum('sales')).order_by('-total_sales')

#     # Productos más vendidos
#     # Se cuenta la cantidad de veces que aparece cada producto en las ventas y se ordena de mayor a menor
#     best_selling_products = Sale.objects.values('product_name').annotate(total_sales=Count('product_name')).order_by('-total_sales')

#     # Contexto para pasar a la plantilla
#     context = {
#         "year_sales_total": year_sales_total,  # Total de ventas en el año 2017
#         "year_sales_amount": year_sales_amount,  # Cantidad de ventas en el año 2017
#         "avg_delivery_time": avg_delivery_time,  # Tiempo de entrega promedio en horas
#         "avg_income_per_customer": avg_income_per_customer,  # Ingreso promedio por cliente
#         "sales_amount_per_state": sales_amount_per_state,  # Total de ventas por estado
#         "best_selling_products": best_selling_products  # Productos más vendidos
#     }
#     return render(request, 'vista_general.html', context)


# PRUEBAS IMPORTANTES NO MODIFICAR PORFA 
def verify_data(request):
    sales = Sale.objects.all()[:20]  # Obtener los primeros 10 registros
    return render(request, 'verify_data.html', {'sales': sales})

# ==================== PEDIDOS =========================================
def pedidos(request):

    avg_delivery_time_per_ship_mode = round(df.groupby('Ship Mode')['delivery'].mean())
    avg_delivery_time_per_ship_mode = avg_delivery_time_per_ship_mode.to_json(orient='records')
    
    monthly_delivery_time = round(df.groupby(["year","month"])['delivery'].mean().dt.total_seconds() / 3600,3)
    monthly_delivery_time = monthly_delivery_time.to_json(orient='records')

    orders = df[['Order ID','Customer Name','Order Date','Ship Date','delivery']]
    orders = orders.to_json(orient='records')

    context = {
        "avg_delivery_time_per_ship_mode": avg_delivery_time_per_ship_mode,
        "monthly_delivery_time" : monthly_delivery_time,
        "orders": orders
    }
    
    return render(request, 'pedidos.html', context)


# ==================== PRODUCTOS ======================================
def productos(request):

    best_selling_sub_categories = df.groupby("Sub-Category")["Sales"].sum().reset_index().sort_values("Sales", ascending=False)
    best_selling_sub_categories = best_selling_sub_categories.to_json(orient='records')
    
    products = df.groupby(['Product Name','Category','Sub-Category'])['Sales'].count().reset_index().sort_values("Sales",ascending=False)
    products = products.to_json(orient='records')

    context = {
        "best_selling_sub_categories": best_selling_sub_categories,
        "productos": products
    }
    return render(request, 'productos.html', context)


# ==================== CLIENTES ======================================
def clientes(request):
    
    sales_per_city = df.groupby('City')['Sales'].sum().reset_index().sort_values("Sales",ascending=False)
    sales_per_city = sales_per_city.to_json(orient='records')
    
    most_valuable_customer = df.groupby(['Order ID', 'Customer Name'])['Sales'].sum().reset_index().sort_values("Sales",ascending=False)
    most_valuable_customer = most_valuable_customer.to_json(orient='records')

    customers = df.groupby(["Customer Name"]).agg(total_sales=("Sales","sum"), last_order =('Order Date', 'max')).reset_index().sort_values("total_sales",ascending = False)
    customers = customers.to_json(orient='records')
    
    context = {
        "sales_per_city" : sales_per_city,
        "most_valuable_customer" : most_valuable_customer,
        "customers" : customers
        
    }
    return render(request, 'clientes.html', context)

