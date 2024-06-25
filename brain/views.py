from django.shortcuts import render, redirect
import pandas as pd
from django.db.models import Sum, Count, Avg
from brain.models import Customer, Sale
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Count
from django.shortcuts import render, get_object_or_404
from statsmodels.tsa.statespace.sarimax import SARIMAX


data = pd.read_csv("data/supermarket_sales.csv")
df = data
df['Order Date'] = pd.to_datetime(df['Order Date'], format='%d/%m/%Y')
df['Ship Date'] = pd.to_datetime(df['Ship Date'], format='%d/%m/%Y')

df['day'] = df['Order Date'].dt.day
df['month'] = df['Order Date'].dt.month
df['year'] = df['Order Date'].dt.year
df['delivery'] = df['Ship Date'] - df['Order Date']
df['year_month'] = df['year'].astype(str) + '-' + df['month'].astype(str).str.zfill(2)

clean = df.groupby("year_month")['Sales'].count().reset_index()

# ==================== VISTA GENERAL ====================================
def overview(request):
    sales_per_year = df.groupby('year')['Sales'].agg('sum').reset_index()  
    sales_per_year = sales_per_year.to_json(orient='records')

    year_sales_total =  "{:,.2f}".format(round(df['Sales'].sum(), 2))
    year_sales_amount = df['Sales'].count()
    
    avg_delivery_time = int((df['delivery'].dt.total_seconds() / 3600).mean())

    avg_income_per_customer = round(((df.groupby("Customer ID")['Sales'].sum()).reset_index()['Sales']).mean(), 2)

    sales_amount_per_state = df.groupby('State')['Sales'].sum().reset_index().sort_values("Sales", ascending=False)
    sales_amount_per_state = sales_amount_per_state.nlargest(10, 'Sales').reset_index(drop=True)
    sales_amount_per_state = sales_amount_per_state.to_json(orient='records')

    monthly_sales_2015 = df.groupby(['year','month'])['Sales'].sum()[2015].reset_index()
    monthly_sales_2015 = monthly_sales_2015.to_json(orient='records')

    monthly_sales_2016 = df.groupby(['year','month'])['Sales'].sum()[2016].reset_index()
    monthly_sales_2016 = monthly_sales_2016.to_json(orient='records')

    monthly_sales_2017 = df.groupby(['year','month'])['Sales'].sum()[2017].reset_index()
    monthly_sales_2017 = monthly_sales_2017.to_json(orient='records')

    monthly_sales_2018 = df.groupby(['year','month'])['Sales'].sum()[2018].reset_index()
    monthly_sales_2018 = monthly_sales_2018.to_json(orient='records')

    best_products = df.groupby('Product Name')['Sales'].agg("sum").nlargest(15).reset_index()
    best_products = best_products.rename(columns={'Product Name': 'product', 'Sales': 'sales'}).to_dict('records')

    context = { 
        "sales_per_year": sales_per_year,
        "year_sales_total": year_sales_total,
        "year_sales_amount": year_sales_amount,
        "avg_delivery_time": avg_delivery_time,
        "avg_income_per_costumer": avg_income_per_customer,
        "sales_amount_per_state": sales_amount_per_state,
        "monthly_sales_2015":monthly_sales_2015,
        "monthly_sales_2016":monthly_sales_2016,
        "monthly_sales_2017":monthly_sales_2017,
        "monthly_sales_2018":monthly_sales_2018,
        "best_products":best_products,
        "active": 1
    }
    return render(request, 'overview.html', context)

# ==================== PEDIDOS =========================================
def orders(request):
    # Calcular tiempo promedio de entrega por modo de envío (excluyendo 'Same Day')
    avg_delivery_time_per_ship_mode = round(df.groupby('Ship Mode')['delivery'].mean().dt.total_seconds() / 3600, 3).reset_index()
    avg_delivery_time_per_ship_mode = avg_delivery_time_per_ship_mode[avg_delivery_time_per_ship_mode['Ship Mode'] != 'Same Day']
    avg_delivery_time_per_ship_mode = avg_delivery_time_per_ship_mode.to_json(orient='records')

    # Ajustar modelo SARIMAX
    model = SARIMAX(clean['Sales'], order=(0, 1, 1), seasonal_order=(0, 1, 1, 12))
    model_fit = model.fit()

    # Índice de inicio y fin para las predicciones
    start_idx = clean.index[-1]  # Predecir desde el último índice actual
    end_idx = start_idx + 11  # Predicciones por 12 meses

    predictions = model_fit.predict(start=start_idx, end=end_idx, dynamic=True)
    prediction_x_values = list(predictions.index)
    prediction_y_values = list(predictions)

    # Calcular horas promedio de entrega por mes y año
    average_delivery_hours = df.groupby(["year", "month"])['delivery'].mean().dt.total_seconds() / 3600
    average_delivery_hours = average_delivery_hours.reset_index()
    average_delivery_hours['date'] = average_delivery_hours['month'].astype(str) + '-' + average_delivery_hours['year'].astype(str)
    
    result_data = average_delivery_hours[['date', 'delivery']].copy()
    result_data.columns = ['date', 'average_delivery_hours']
    result_data['average_delivery_hours'] = result_data['average_delivery_hours'].round(3)
    result_data = result_data.to_json(orient='records')

    # Calcular cantidad de ventas por mes y año
    amount_of_sales_per_month_and_year = df.groupby('year_month')['Sales'].count().reset_index()
    amount_of_sales_per_month_and_year = amount_of_sales_per_month_and_year.to_json(orient='records')

    # Obtener todos los pedidos ordenados por fecha de pedido
    orders = Sale.objects.all().order_by('-order_date')

    # Número de página actual
    page_number = request.GET.get('page', 1)

    # Paginar los resultados
    paginator = Paginator(orders, 10)  # 10 elementos por página

    try:
        page_obj = paginator.page(page_number)
    except PageNotAnInteger:
        # Si el parámetro de la página no es un número, mostrar la primera página
        page_obj = paginator.page(1)
    except EmptyPage:
        # Si la página está fuera de rango (página 9999), mostrar la última página de resultados
        page_obj = paginator.page(paginator.num_pages)

    # Pasar objetos de página a la plantilla
    context = {
        "page_obj": page_obj,
        "avg_delivery_time_per_ship_mode": avg_delivery_time_per_ship_mode,
        "monthly_delivery_time": result_data,
        "amount_of_sales_per_month_and_year": amount_of_sales_per_month_and_year,
        "active": 2,
        "prediction_x_values": prediction_x_values,
        "prediction_y_values": prediction_y_values,
    }

    return render(request, 'orders.html', context)



# ==================== PRODUCTOS ======================================
def products(request):
    best_selling_sub_categories = df.groupby("Sub-Category")["Sales"].sum().nlargest(10).reset_index().sort_values("Sales", ascending=False)
    best_selling_sub_categories = best_selling_sub_categories.to_json(orient='records')

    best_segments = df.groupby('Segment')['Sales'].agg("sum").reset_index()
    best_segments = best_segments.to_json(orient='records')

    top_3_selling_2015 = df[df['year'] == 2015].groupby('Product Name')['Sales'].sum().nlargest(5).reset_index().round(2)
    top_3_selling_2015 = top_3_selling_2015.rename(columns={'Product Name': 'ProductName', 'Sales': 'TotalSales'}).to_dict('records')

    top_3_selling_2016 = df[df['year'] == 2016].groupby('Product Name')['Sales'].sum().nlargest(5).reset_index().round(2)
    top_3_selling_2016 = top_3_selling_2016.rename(columns={'Product Name': 'ProductName', 'Sales': 'TotalSales'}).to_dict('records')

    top_3_selling_2017 = df[df['year'] == 2017].groupby('Product Name')['Sales'].sum().nlargest(5).reset_index().round(2)
    top_3_selling_2017 = top_3_selling_2017.rename(columns={'Product Name': 'ProductName', 'Sales': 'TotalSales'}).to_dict('records')

    top_3_selling_2018 = df[df['year'] == 2018].groupby('Product Name')['Sales'].sum().nlargest(5).reset_index().round(2)
    top_3_selling_2018 = top_3_selling_2018.rename(columns={'Product Name': 'ProductName', 'Sales': 'TotalSales'}).to_dict('records')

    page_number = request.GET.get('page', 1)

    best_selling_products_query = (Sale.objects
        .values('product_name', 'category', 'sub_category')
        .annotate(sales_count=Count('product_name'))
        .order_by('-sales_count'))

    paginator = Paginator(best_selling_products_query, 14)

    try:
        best_selling_products_page = paginator.page(page_number)
    except PageNotAnInteger:
        best_selling_products_page = paginator.page(1)
    except EmptyPage:
        best_selling_products_page = paginator.page(paginator.num_pages)

    
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
        "best_selling_sub_categories": best_selling_sub_categories,
        "active": 3,
        "best_selling_products": best_selling_products_list, 
        "best_segments":best_segments,
        "top_3_selling_2015":top_3_selling_2015,
        "top_3_selling_2016":top_3_selling_2016,
        "top_3_selling_2017":top_3_selling_2017,
        "top_3_selling_2018":top_3_selling_2018,
        "pagination":  {
            "first_page":1,
            "last_page":paginator.num_pages,
            "active_page":page_number,
            "pages":pages
        },
    }
    return render(request, 'products.html', context)

# ==================== CLIENTES ======================================
def customers(request):
    sales_per_city = df.groupby('City')['Sales'].sum().reset_index().sort_values("Sales",ascending=False)
    sales_per_city = sales_per_city.nlargest(10, 'Sales').reset_index(drop=True)
    sales_per_city = sales_per_city.to_json(orient='records')
    
    top_10_customers = df.groupby('Customer Name')['Sales'].agg('sum').nlargest(10).reset_index()
    top_10_customers = top_10_customers.rename(columns={'Customer Name': 'name', 'Sales': 'sales'}).to_dict('records')

    avg_revenue_perClient_year = df.groupby(["year", "Customer ID"])['Sales'].sum().groupby("year").mean().reset_index()
    avg_revenue_perClient_year = avg_revenue_perClient_year.to_json(orient="records")
    
    total_amount_of_customers = Customer.objects.count()
    customers_list = Customer.objects.all()
    paginator = Paginator(customers_list, 20)  

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'customers.html', {
        'page_obj': page_obj,
        'sales_per_city': sales_per_city,
        "top_10_customers":top_10_customers,
        "avg_revenue_perClient_year":avg_revenue_perClient_year,
        "total_amount_of_customers":total_amount_of_customers,
        "active":4
        })

def customer_detail(request, customer_id):
    customer = get_object_or_404(Customer, pk=customer_id)
    orders = Sale.objects.filter(customer_id=customer_id)

    return render(request, 'customer_detail.html', {'customer': customer, 'orders': orders,"active":4 })