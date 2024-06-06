# Create your views here.
from django.shortcuts import render, redirect
import csv
import pandas as pd
from django.db.models import Sum, Count, Avg
from brain.models import Customer, Sale
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Count
from django.shortcuts import render, get_object_or_404
data = pd.read_csv("data/supermarket_sales.csv")
df = data
df['Order Date'] = pd.to_datetime(df['Order Date'], format='%d/%m/%Y')
df['Ship Date'] = pd.to_datetime(df['Ship Date'], format='%d/%m/%Y')

df['day'] = df['Order Date'].dt.day
df['month'] = df['Order Date'].dt.month
df['year'] = df['Order Date'].dt.year
df['delivery'] = df['Ship Date'] - df['Order Date']

# ==================== VISTA GENERAL ====================================
def vista_general(request):
    sales_per_year = df.groupby('year')['Sales'].agg('sum').reset_index()  
    sales_per_year = sales_per_year.to_json(orient='records')

    year_sales_total =  "{:,.2f}".format(round(df['Sales'].sum(), 2))
    year_sales_amount = df[df['year'] == 2017]['Sales'].count()
    
    avg_delivery_time = int((df['delivery'].dt.total_seconds() / 3600).mean())

    avg_income_per_customer = round(((df.groupby("Customer ID")['Sales'].sum()).reset_index()['Sales']).mean(), 2)

    sales_amount_per_state = df.groupby('State')['Sales'].sum().reset_index().sort_values("Sales", ascending=False)
    sales_amount_per_state = sales_amount_per_state.nlargest(10, 'Sales').reset_index(drop=True)
    sales_amount_per_state = sales_amount_per_state.to_json(orient='records')

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
        "sales_per_year": sales_per_year,
        "year_sales_total": year_sales_total,
        "year_sales_amount": year_sales_amount,
        "avg_delivery_time": avg_delivery_time,
        "avg_income_per_costumer": avg_income_per_customer,
        "sales_amount_per_state": sales_amount_per_state,
        "best_selling_products": best_selling_products_list, 
        "pagination":  {
            "first_page":1,
            "last_page":paginator.num_pages,
            "active_page":page_number,
            "pages":pages
        },
        "active": 1
    }
    return render(request, 'vista_general.html', context)

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
    paginator = Paginator(orders, 20) 
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        "avg_delivery_time_per_ship_mode": avg_delivery_time_per_ship_mode,
        "monthly_delivery_time": result_data,
        "page_obj": page_obj, 
        "active": 2
    }
    
    return render(request, 'pedidos.html', context)


# ==================== PRODUCTOS ======================================
def productos(request):
    best_selling_sub_categories = df.groupby("Sub-Category")["Sales"].sum().reset_index().sort_values("Sales", ascending=False)
    best_selling_sub_categories = best_selling_sub_categories.to_json(orient='records')

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
        "pagination":  {
            "first_page":1,
            "last_page":paginator.num_pages,
            "active_page":page_number,
            "pages":pages
        },
    }
    return render(request, 'productos.html', context)

# ==================== CLIENTES ======================================
def show_all_customers(request):
    sales_per_city = df.groupby('City')['Sales'].sum().reset_index().sort_values("Sales",ascending=False)
    sales_per_city = sales_per_city.nlargest(10, 'Sales').reset_index(drop=True)
    sales_per_city = sales_per_city.to_json(orient='records')

    customers_list = Customer.objects.all()
    paginator = Paginator(customers_list, 20)  

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