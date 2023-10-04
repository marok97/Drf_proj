from django.db import models
from mptt.models import MPTTModel, TreeForeignKey

# Create your models here


class Brand(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self) -> str:
        return self.name


class Category(MPTTModel):
    name = models.CharField(max_length=100)
    parent = TreeForeignKey(
        "self",
        on_delete=models.PROTECT,
        null=True,
        blank=True,
    )

    class MPTTMeta:
        order_insertion_by = ["name"]

    def __str__(self) -> str:
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(max_length=200, blank=True)
    is_digital = models.BooleanField(default=False)
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE)
    category = TreeForeignKey(
        "Category", null=True, blank=True, on_delete=models.SET_NULL
     )

    def __str__(self) -> str:
        return self.name


# class ProductLine(models.Model):
#     price = models.DecimalField()
#     sku = models.CharField()
#     stock_quantity = models.IntegerField()
#     product = models.ForeignKey(Product, on_delete=models.CASCADE)


# class ProductImage(models.Model):
#     name = models.CharField()
#     alternative_text = models.CharField()
#     url = models.ImageField()
#     product_line = models.ForeignKey(ProductLine)

#     def __str__(self) -> str:
#         return self.name


# class Attribute(models.Model):
#     name = models.CharField()

#     def __str__(self) -> str:
#         return self.name


# class AttributeValue(models.Model):
#     value = models.CharField()
#     attribute = models.ForeignKey(Attribute)
