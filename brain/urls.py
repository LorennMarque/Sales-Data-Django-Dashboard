from django.urls import path
from . import views

urlpatterns = [
    path('view', views.visualize_data, name='visualize_data'),
    path('describe', views.data_describe, name='descriptions'),
    path("nav", views.nav, name="nav"),
    path("", views.vista_general, name="inicio"),
    path("pedidos", views.pedidos, name="pedidos"),
    path("clientes", views.clientes, name="clientes"),
    path("productos", views.productos, name="productos")
    
]