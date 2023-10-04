from django.db import models

# Create your models here


class Product(models.Model):
    name = models.CharField(max_length=30)
    description = models.TextField(max_length=200)
    type = models.CharField(max_length=30)


class Category(models.Model):
    name = models.CharField(max_length=30)
    product = models.ManyToManyField(Product)


class ProductLine(models.Model):
    price = models.DecimalField()
    sku = models.CharField()
    stock_quantity = models.IntegerField()
    product = models.ForeignKey(Product, on_delete=models.CASCADE)


class ProductImage(models.Model):
    name = models.CharField()
    alternative_text = models.CharField()
    url = models.ImageField()
    product_line = models.ForeignKey(ProductLine)


class Attribute(models.Model):
    name = models.CharField()


class AttributeValue(models.Model):
    value = models.CharField()
    attribute = models.ForeignKey(Attribute)
