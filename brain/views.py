from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect
from brain.models import Sale
import csv

def visualize_data(request):
    # sales = Sales.objects.order_by('-date') # menor a mayor default. Incluir el - para invertir
    
    with open ("data/supermarket_sales.csv" , "r") as f:
        data = csv.reader(f)
        sales = [] # Lista de objetos

        for row in data:
            # 1. Revisar si la primera fila es un encabezado      
            is_header = row[0] == "Invoice ID"
            
            if not is_header:
                created = Sale(
                        invoice_id = row[0],
                        branch = row[1],
                        city = row[2],
                        costumer_type = row[3], 
                        gender = row[4], 
                        product_line = row[5],
                        unit_price = row[6],
                        quantity = row[7],
                        tax = row[8], 
                        total = row[9],
                        date = row[10],
                        time = row[11],
                        payment = row[12],
                        cogs = row[13],
                        gross_margin_percentage = row[14],
                        gross_income = row[15],
                        rating = row[16] )
                # Agregamos la venta creada a la lista                # Agregamos la venta creada a la lista
                sales.append(created)

    context = {
    "sales" : sales
    }

    return render(request, 'visualize_data.html', context)

# from django.shortcuts import render
# from django.http import HttpResponse
# from django.template import loader

# from pollapp.models import Question

# def index(request):
#     questions = Question.objects.order_by('-date') # menor a mayor default. Incluir el - para invertir

#     context = {
#         "questions":questions
#     }

#     return render(request, "index.html", context)

# def detail(request, question_id):
#     return HttpResponse(f"This is the question number {question_id}")
