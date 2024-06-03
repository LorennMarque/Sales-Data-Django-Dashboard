from django.core.management.base import BaseCommand
from brain.models import Sale
import pandas as pd

class Command(BaseCommand):
    help = 'Load data from CSV into the Sale model'

    def handle(self, *args, **kwargs):
        data = pd.read_csv("data/supermarket_sales.csv")
        data['Order Date'] = pd.to_datetime(data['Order Date'], format='%d/%m/%Y')
        data['Ship Date'] = pd.to_datetime(data['Ship Date'], format='%d/%m/%Y')
        sales = [
            Sale(
                row_id=row['Row ID'],
                order_id=row['Order ID'],
                order_date=row['Order Date'],
                ship_date=row['Ship Date'],
                ship_mode=row['Ship Mode'],
                customer_id=row['Customer ID'],
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
            for _, row in data.iterrows()
        ]
        Sale.objects.bulk_create(sales)
        self.stdout.write(self.style.SUCCESS('Data loaded successfully'))
