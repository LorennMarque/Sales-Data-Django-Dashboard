from django.db import models
import pandas as pd

# Create your models here.
data = pd.read_csv("data/supermarket_sales.csv")
# print(data)

# Create your models here.
# class Question (models.Model):
#     question_text = models.CharField(max_length=200)
#     date = models.DateTimeField()

#     def __str__(self):
#         return self.question_text

# class Answer (models.Model):
#     answer_text = models.CharField(max_length=200)
#     date = models.DateTimeField()
#     question = models.ForeignKey(Question, on_delete=models.CASCADE)
#     likes = models.IntegerField(default=0)

#     def __str__(self):
#         return self.answer_text
    
#     def is_popular (self):
#         return self.likes >= 3

class Sale(models.Model):
    # Invoice ID,
    invoice_id = models.CharField(max_length=255)
    # Branch,
    branch = models.CharField(max_length=1)
    # City,
    city = models.CharField(max_length=20)
    # Customer type,
    costumer_type = models.CharField(max_length=10) # Pero el máximo sería 6, Member ó Normal
    # Gender,
    gender = models.CharField(max_length=10) # Pero el máximo sería 6, Fermale ó Male
    # Product line,
    product_line = models.CharField(max_length=255)
    # Unit price,
    unit_price = models.FloatField()
    # Quantity,
    quantity = models.FloatField()
    # Tax 5%,
    tax = models.CharField(max_length=10) # Pero el máximo sería 6, Fermale ó Male
    # Total,
    total = models.FloatField()
    # Date,
    date = models.DateField()
    # Time,
    time = models.TimeField()
    # Payment,
    payment = models.CharField(max_length=10)
    # cogs,
    cogs = models.FloatField()
    # gross margin percentage,
    gross_margin_percentage = models.FloatField()
    # gross income,
    gross_income = models.FloatField()
    # Rating
    rating = models.FloatField()
