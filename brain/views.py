# Create your views here.
from django.shortcuts import render, redirect
import csv
import pandas as pd
import matplotlib.pyplot as plt
from django.db.models import Sum, Count, Avg
from brain.models import Customer, Sale
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Count
from django.core.serializers.json import DjangoJSONEncoder
from django.shortcuts import render, get_object_or_404
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

def content(request):
    context = {
        "sales_per_year": "hola",
    }

    return render(request, 'content.html', context)




# ==================== VISTA GENERAL ====================================
def vista_general(request):
    sales_per_year = df.groupby('year')['Sales'].agg('sum').reset_index()  
    sales_per_year = sales_per_year.to_json(orient='records')

    # 1. Guardar una variable con los datos
    year_sales_total =  "{:,.2f}".format(round(df['Sales'].sum(), 2))
    year_sales_amount = df[df['year'] == 2017]['Sales'].count()
    
    avg_delivery_time = int((df['delivery'].dt.total_seconds() / 3600).mean())

    avg_income_per_customer = round(((df.groupby("Customer ID")['Sales'].sum()).reset_index()['Sales']).mean(), 2)

    sales_amount_per_state = df.groupby('State')['Sales'].sum().reset_index().sort_values("Sales", ascending=False)
    sales_amount_per_state = sales_amount_per_state.nlargest(10, 'Sales').reset_index(drop=True)
    sales_amount_per_state = sales_amount_per_state.to_json(orient='records')


    # results = int(request.GET.get('page', ''))

    # # Realizar la consulta para contar las ventas por producto
    # best_selling_products = (Sale.objects
    #     .values('product_name', 'category', 'sub_category')
    #     .annotate(sales_count=Count('product_name'))
    #     .order_by('-sales_count')[:results])

    # # Renombrar los campos según sea necesario, así es más facil de leer y convertir los resultados a una lista de diccionarios
    # best_selling_products = [{
    #     'Product': item['product_name'],
    #     'MainCategory': item['category'],
    #     'Subcategory': item['sub_category'],
    #     'Sales': item['sales_count']
    # } for item in best_selling_products]

    # # Convertir la lista de diccionarios a JSON
    # best_selling_products = json.dumps(best_selling_products, cls=DjangoJSONEncoder)

        # Crear un paginador con 20 resultados por página

    page_number = request.GET.get('page', 1)

    best_selling_products_query = (Sale.objects
        .values('product_name', 'category', 'sub_category')
        .annotate(sales_count=Count('product_name'))
        .order_by('-sales_count'))

    paginator = Paginator(best_selling_products_query, 14)

    try:
        # Obtener la página solicitada
        best_selling_products_page = paginator.page(page_number)
    except PageNotAnInteger:
        # Si el número de página no es un entero, mostrar la primera página
        best_selling_products_page = paginator.page(1)
    except EmptyPage:
        # Si el número de página está fuera del rango, mostrar la última página
        best_selling_products_page = paginator.page(paginator.num_pages)

    # Formatear los resultados y convertirlos a una lista de diccionarios
    best_selling_products_list = [{
        'Product': item['product_name'],
        'MainCategory': item['category'],
        'Subcategory': item['sub_category'],
        'Sales': item['sales_count']
    } for item in best_selling_products_page]

    page_number = int(page_number)
    if page_number <= 3:
        pages = [1,2,3,4,5]
    elif page_number <= paginator.num_pages - 4:
        pages = [page_number-2,page_number-1,page_number,page_number+1,page_number+2]
    else:
        pages = [paginator.num_pages-4,paginator.num_pages-3,paginator.num_pages-2,paginator.num_pages-1,paginator.num_pages]

    context = {
        "sales_per_year": sales_per_year,
        "year_sales_total": year_sales_total,
        "year_sales_amount": year_sales_amount,
        "avg_delivery_time": avg_delivery_time,
        "avg_income_per_costumer": avg_income_per_customer,
        "sales_amount_per_state": sales_amount_per_state,
        "best_selling_products": best_selling_products_list,  # Pass the list directly
        "pagination":  {
            "first_page":1,
            "last_page":paginator.num_pages,
            "active_page":page_number,
            "pages":pages
        },
        "active": 1
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
    avg_delivery_time_per_ship_mode = round(df.groupby('Ship Mode')['delivery'].mean().dt.total_seconds() / 3600, 3).reset_index()
    avg_delivery_time_per_ship_mode = avg_delivery_time_per_ship_mode.to_json(orient='records')
    
    average_delivery_hours = df.groupby(["year", "month"])['delivery'].mean().dt.total_seconds() / 3600
    average_delivery_hours = average_delivery_hours.reset_index()
    average_delivery_hours['date'] = average_delivery_hours['month'].astype(str) + '-' + average_delivery_hours['year'].astype(str)
    result_data = average_delivery_hours[['date', 'delivery']]
    result_data.columns = ['date', 'average_delivery_hours']
    result_data['average_delivery_hours'] = result_data['average_delivery_hours'].round(3)
    result_data = result_data.to_json(orient='records')

    orders = Sale.objects.all().order_by('-order_date')


    # Paginación
    paginator = Paginator(orders, 20)  # 10 registros por página
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        "avg_delivery_time_per_ship_mode": avg_delivery_time_per_ship_mode,
        "monthly_delivery_time": result_data,
        "page_obj": page_obj,  # Pasar el objeto de página a la plantilla
        "active": 2
    }
    
    return render(request, 'pedidos.html', context)


# ==================== PRODUCTOS ======================================
def productos(request):
    # Suponiendo que 'df' es tu DataFrame ya cargado
    best_selling_sub_categories = df.groupby("Sub-Category")["Sales"].sum().reset_index().sort_values("Sales", ascending=False)
    best_selling_sub_categories = best_selling_sub_categories.to_json(orient='records')
    
    products = df.groupby(['Product Name','Category','Sub-Category'])['Sales'].count().reset_index().sort_values("Sales", ascending=False)
    products = products.rename(columns={'Product Name': 'Product', 'Category': 'MainCategory', 'Sub-Category': 'Subcategory', 'Sales': 'Sales'})
    products = products.to_dict(orient='records')

    context = {
        "best_selling_sub_categories": best_selling_sub_categories,
        "productos": products,
        "active": 3
    }
    return render(request, 'productos.html', context)

# ==================== CLIENTES ======================================
def show_all_customers(request):
    sales_per_city = df.groupby('City')['Sales'].sum().reset_index().sort_values("Sales",ascending=False)
    sales_per_city = sales_per_city.nlargest(10, 'Sales').reset_index(drop=True)
    sales_per_city = sales_per_city.to_json(orient='records')

    customers_list = Customer.objects.all()
    paginator = Paginator(customers_list, 20)  # Show 20 customers per page.

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'all_customers.html', {
        'page_obj': page_obj,
        'sales_per_city': sales_per_city,
        "active":4
        })

def show_customer_details(request, customer_id):
    customer = get_object_or_404(Customer, pk=customer_id)
    orders = Sale.objects.filter(customer_id=customer_id)

    return render(request, 'customer_details.html', {'customer': customer, 'orders': orders,"active":4 })