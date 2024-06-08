from django.urls import path
from . import views

urlpatterns = [
    path("", views.overview, name="overview"),
    path("orders", views.orders, name="orders"),
    path("products", views.products, name="products"),
    path('customers/', views.customers, name='customers'),
    path('customers/<int:customer_id>/', views.customer_detail, name='customer_detail'),
]