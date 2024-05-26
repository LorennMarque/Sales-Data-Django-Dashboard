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
    # Row ID,
    row_id = models.FloatField()
    # Order ID,
    order_id = models.CharField(max_length=255)
    # Order Date,
    order_date = models.DateField()
    # ship_date,
    ship_date = models.DateField(max_length=255) 
    # ship_mode,
    ship_mode = models.CharField(max_length=255)
    # customer_id,
    customer_id = models.CharField(max_length=255)
    # customer_name,
    customer_name = models.CharField(max_length=255)
    # segment,
    segment = models.CharField(max_length=255)
    # country,
    country = models.CharField(max_length=255)
    # city,
    city = models.CharField(max_length=255)
    # state,
    state = models.CharField(max_length=255)
    # postal_code,
    postal_code = models.FloatField()
    # region,
    region = models.CharField(max_length=255)
    # product_id,
    product_id = models.CharField(max_length=255)
    # category,
    category = models.CharField(max_length=255)
    # sub_category,
    sub_category = models.CharField(max_length=255)
    # gross product_name,
    product_name = models.FloatField()
    # sales
    sales = models.FloatField()
