from django.urls import path
from . import views

urlpatterns = [
    path('view', views.visualize_data, name='visualize_data'),
    # path('describe', views.data_describe, name='descriptions'),
    # path("nav", views.nav, name="nav"),
    path("", views.vista_general, name="inicio"),
    path("orders", views.pedidos, name="pedidos"),
    path("products", views.productos, name="productos"),
    path('verify-data/', views.verify_data, name='verify_data'),
    path('customers/', views.show_all_customers, name='all_customers'),
    path('customers/<int:customer_id>/', views.show_customer_details, name='customer_details'),
    path('content/', views.content, name='content')
]