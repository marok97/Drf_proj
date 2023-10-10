from rest_framework import serializers
from .models import (
    Product,
    Category,
    Brand,
    ProductLine,
    ProductImage,
    Attribute,
    AttributeValue,
)


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


class AttributeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attribute
        fields = ["name", "id"]


class AttributeValueSerializer(serializers.ModelSerializer):
    attribute = AttributeSerializer(many=False)

    class Meta:
        model = AttributeValue
        fields = "__all__"


class ProductLineSerializer(serializers.ModelSerializer):
    # Passes in the related product image by "related_name" in model. so called "reverse FK"
    product_image = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    attribute_value = AttributeValueSerializer(many=True)

    class Meta:
        model = ProductLine
        exclude = ("id", "is_active", "product")

    def to_representation(self, instance):
        repr = super().to_representation(instance)
        av_data = repr.pop("attribute_value")
        av_values = {}
        for key in av_data:
            av_values.update({key["attribute"]["id"]: key["value"]})

        repr.update({"specification": av_values})
        return repr


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
