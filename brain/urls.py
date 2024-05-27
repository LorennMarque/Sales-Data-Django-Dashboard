from django.urls import path
from . import views

urlpatterns = [
    path('view', views.visualize_data, name='visualize_data'),
    path('describe', views.data_describe, name='descriptions'),
    path("", views.panel_principal, name="inicio"),
    path("nav", views.nav, name="nav")
]