from rest_framework import serializers
from .models import Product, Category, Brand, ProductLine, ProductImage


class CategorySerializer(serializers.ModelSerializer):
    # Makes name in category model show up as "category"
    category = serializers.CharField(source="name")

    class Meta:
        model = Category
        # Uses only "category" from model as viewable in API
        fields = ["category"]


class BrandSerializer(serializers.ModelSerializer):
    # Makes name in brand model show up as "brand"
    brand = serializers.CharField(source="name")

    class Meta:
        model = Brand
        # Excludes id from showing up in API view
        exclude = ("id",)


class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ["url", "alternative_text", "order"]

class ProductLineSerializer(serializers.ModelSerializer):
    # Passes in the related product image by "related_name" in model. so called "reverse FK"
    product_image = ProductImageSerializer(many=True)
    class Meta:
        model = ProductLine
        exclude = ("id", "is_active", "product")


class ProductSerializer(serializers.ModelSerializer):
    # Gets Brand related to product by FK
    brand = serializers.ReadOnlyField(source="brand.name")
    # Gets Category related to product by FK
    category = serializers.ReadOnlyField(source="category.name")

    # Passes in the related ProductLines by "related_name" in model. so called "reverse FK"
    product_line = ProductLineSerializer(many=True)

    class Meta:
        model = Product
        fields = [
            "name",
            "slug",
            "description",
            "is_digital",
            "brand",
            "category",
            "product_line",
        ]
