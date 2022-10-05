from django.db import models
from django.contrib.auth.models import User

GENDER_CHOICES = [
    ("Donna", "Donna"),
    ("Uomo", "Uomo"),
]


class Product(models.Model):
    product_id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=100)
    brand = models.CharField(max_length=80)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES,)
    price = models.IntegerField()
    size = models.CharField(max_length=100, default=None)
    color = models.CharField(max_length=100, default=None)
    category = models.CharField(max_length=100)
    description = models.TextField()
    care = models.TextField()
    image_urls = models.TextField()

    def __int__(self):
        return self.product_id

    def __str__(self):
        return self.title


class Order(models.Model):
    order_id = models.AutoField(primary_key=True)
    username = models.ForeignKey(User, on_delete=models.CASCADE)
    product_id = models.ForeignKey(Product, on_delete=models.CASCADE)
    status = models.CharField(max_length=10, default='unpaid')
    quantity = models.IntegerField()
    size = models.CharField(max_length=10)
    color = models.CharField(max_length=20)

    def __int__(self):
        return self.order_id
