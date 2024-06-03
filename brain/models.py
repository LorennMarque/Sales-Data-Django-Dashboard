from django.db import models

class Sale(models.Model):
    row_id = models.IntegerField()  # Cambiado a IntegerField
    order_id = models.CharField(max_length=255)
    order_date = models.DateField()
    ship_date = models.DateField()
    ship_mode = models.CharField(max_length=255)
    customer_id = models.CharField(max_length=255)
    customer_name = models.CharField(max_length=255)
    segment = models.CharField(max_length=255)
    country = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    state = models.CharField(max_length=255)
    postal_code = models.CharField(max_length=20)  # Cambiado a CharField
    region = models.CharField(max_length=255)
    product_id = models.CharField(max_length=255)
    category = models.CharField(max_length=255)
    sub_category = models.CharField(max_length=255)
    product_name = models.CharField(max_length=255)
    sales = models.FloatField()
    delivery_time = models.DurationField(null=True, blank=True)

    def save(self, *args, **kwargs):
        if self.order_date and self.ship_date:
            self.delivery_time = self.ship_date - self.order_date
        super().save(*args, **kwargs)
