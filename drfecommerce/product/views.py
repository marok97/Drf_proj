from django.shortcuts import get_object_or_404, render
from django.db.models import Prefetch
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from drf_spectacular.utils import extend_schema
from .models import Category, Brand, Product
from .serializers import CategorySerializer, BrandSerializer, ProductSerializer


class CategoryView(viewsets.ViewSet):
    queryset = Category.objects.all()

    @extend_schema(responses=CategorySerializer)
    def list(self, request):
        serializer = CategorySerializer(self.queryset, many=True)
        data = serializer.data

        return Response(data, status=status.HTTP_200_OK)


class BrandView(viewsets.ViewSet):
    queryset = Brand.objects.all()

    @extend_schema(responses=BrandSerializer)
    def list(self, request):
        serializer = BrandSerializer(self.queryset, many=True)
        data = serializer.data

        return Response(data, status=status.HTTP_200_OK)


class ProductView(viewsets.ViewSet):
    queryset = Product.objects.all().where_is_active()
    lookup_field = "slug"

    @extend_schema(responses=ProductSerializer)
    def list(self, request):
        serializer = ProductSerializer(
            self.queryset.select_related("category", "brand"), many=True
        )
        data = serializer.data

        return Response(data, status=status.HTTP_200_OK)

    @extend_schema(responses=ProductSerializer)
    def retrieve(self, request, slug=None):
        # Use select_related with foreign keyes to minimize number of queries to DB by utilizing "SQL JOINS" and speed up the query
        # select_related is not possible with "reverse foreign keys" as the "slug" from the ProductLine model. Instead use "prefetch_related"

        query = (
            self.queryset.filter(slug=slug)
            .select_related("category", "brand")
            .prefetch_related(Prefetch("product_line__product_image"))
        )
        serializer = ProductSerializer(query, many=True)
        data = serializer.data

        if data:
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(status=status.HTTP_404_NOT_FOUND)

    @action(
        methods=["GET"],
        detail=False,
        url_path=r"category/(?P<category>\w+)/all",
    )

    # Function to filter product by a category
    def product_list_by_category(self, request, category=None):
        serializer = ProductSerializer(
            self.queryset.filter(category__name=category), many=True
        )
        data = serializer.data
        return Response(data, status=status.HTTP_200_OK)

    @action(
        methods=["GET"],
        detail=False,
        url_path=r"brand/(?P<brand>\w+)/all",
    )
    # Function to filter product by a brand
    def product_list_by_brand(self, request, brand=None):
        serializer = ProductSerializer(
            self.queryset.filter(brand__name=brand), many=True
        )
        data = serializer.data
        return Response(data, status=status.HTTP_200_OK)
