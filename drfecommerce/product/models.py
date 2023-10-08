from collections.abc import Iterable
from django.db import models
from mptt.models import MPTTModel, TreeForeignKey
from .fields import OrderField
from django.core.exceptions import ValidationError


# Custom Queryset to filter out non active products
class ActiveQueryset(models.QuerySet):
    def where_is_active(self):
        return self.filter(is_active=True)


class Brand(models.Model):
    name = models.CharField(max_length=100)
    is_active = models.BooleanField(default=False)

    # Make the custom ActiveQueryset accessbile for the default manager
    objects = ActiveQueryset.as_manager()

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
    is_active = models.BooleanField(default=False)
    # Make the custom ActiveQueryset accessbile for the default manager
    objects = ActiveQueryset.as_manager()

    class MPTTMeta:
        order_insertion_by = ["name"]

    def __str__(self) -> str:
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=255)
    description = models.TextField(max_length=200, blank=True)
    is_digital = models.BooleanField(default=False)
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE)
    category = TreeForeignKey(
        "Category", null=True, blank=True, on_delete=models.SET_NULL
    )
    is_active = models.BooleanField(default=False)

    # Default manager for admin
    # Make the custom ActiveQueryset accessbile for the default manager
    objects = ActiveQueryset.as_manager()

    def __str__(self) -> str:
        return self.name


class ProductLine(models.Model):
    price = models.DecimalField(decimal_places=2, max_digits=5)
    # sku = Stock keeping unit
    sku = models.CharField(max_length=100)
    stock_quantity = models.IntegerField()
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="product_line"
    )
    is_active = models.BooleanField(default=False)

    # Custom Field, takes in a unique field in this case the product object
    order = OrderField(blank=True, unique_for_field="product")

    # Make the custom ActiveQueryset accessbile for the default manager
    objects = ActiveQueryset.as_manager()

    # Raises ValidationError if a user tries to create an order with ProductLine id x but that order already exists on ProductLine x
    def clean(self) -> None:
        qs = ProductLine.objects.filter(product=self.product)
        for obj in qs:
            if self.id != obj.id and self.order == obj.order:
                raise ValidationError("Duplicate value.")

    # Makes a full clean before saving and therefore calling "clean" method
    def save(self, *args, **kwargs) -> None:
        self.full_clean()
        return super(ProductLine, self).save(*args, **kwargs)

    def __str__(self) -> str:
        return str(self.order)


class ProductImage(models.Model):
    alternative_text = models.CharField(max_length=100)
    url = models.ImageField(upload_to=None, default="test.jpg")
    product_line = models.ForeignKey(
        ProductLine, on_delete=models.CASCADE, related_name="product_image"
    )
    order = OrderField(blank=True, unique_for_field="product_line")

    # Raises ValidationError if a user tries to create an order with ProductLine id x but that order already exists on ProductLine x
    def clean(self) -> None:
        qs = ProductImage.objects.filter(product_line=self.product_line)
        for obj in qs:
            if self.id != obj.id and self.order == obj.order:
                raise ValidationError("Duplicate value.")

    def save(self, *args, **kwargs) -> None:
        self.full_clean()
        return super(ProductImage, self).save(*args, **kwargs)

    def __str__(self) -> str:
        return str(self.url)


# class Attribute(models.Model):
#     name = models.CharField()

#     def __str__(self) -> str:
#         return self.name


# class AttributeValue(models.Model):
#     value = models.CharField()
#     attribute = models.ForeignKey(Attribute)
