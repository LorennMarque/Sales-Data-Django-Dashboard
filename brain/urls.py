from django.urls import path
from . import views

urlpatterns = [
    path("", views.vista_general, name="inicio"),
    path("orders", views.pedidos, name="pedidos"),
    path("products", views.productos, name="productos"),
    path('customers/', views.show_all_customers, name='all_customers'),
    path('customers/<int:customer_id>/', views.show_customer_details, name='customer_details'),
]