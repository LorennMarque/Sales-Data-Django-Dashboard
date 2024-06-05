from django.core.management.base import BaseCommand
from brain.models import Sale, Customer
import pandas as pd

class Command(BaseCommand):
    help = 'Load data from CSV into the Sale model'

    def handle(self, *args, **kwargs):
        data = pd.read_csv("data/supermarket_sales.csv")
        data['Order Date'] = pd.to_datetime(data['Order Date'], format='%d/%m/%Y')
        data['Ship Date'] = pd.to_datetime(data['Ship Date'], format='%d/%m/%Y')
        sales = []
        customers = set()  # To keep track of unique customers
        for _, row in data.iterrows():
            customer_id = row['Customer ID']
            customers.add(customer_id)
            sale = Sale(
                row_id=row['Row ID'],
                order_id=row['Order ID'],
                order_date=row['Order Date'],
                ship_date=row['Ship Date'],
                ship_mode=row['Ship Mode'],
                customer_id=customer_id,
                customer_name=row['Customer Name'],
                segment=row['Segment'],
                country=row['Country'],
                city=row['City'],
                state=row['State'],
                postal_code=row['Postal Code'],
                region=row['Region'],
                product_id=row['Product ID'],
                category=row['Category'],
                sub_category=row['Sub-Category'],
                product_name=row['Product Name'],
                sales=row['Sales'],
            )
            sales.append(sale)
        
        Sale.objects.bulk_create(sales)
        
        # Create customers
        customer_objects = [
            Customer(
                customer_id=customer_id,
                customer_name=data[data['Customer ID'] == customer_id]['Customer Name'].iloc[0],
                country=data[data['Customer ID'] == customer_id]['Country'].iloc[0],
                city=data[data['Customer ID'] == customer_id]['City'].iloc[0],
                state=data[data['Customer ID'] == customer_id]['State'].iloc[0],
                postal_code=data[data['Customer ID'] == customer_id]['Postal Code'].iloc[0],
                region=data[data['Customer ID'] == customer_id]['Region'].iloc[0],
            )
            for customer_id in customers
        ]
        Customer.objects.bulk_create(customer_objects)

        self.stdout.write(self.style.SUCCESS('Data loaded successfully'))
