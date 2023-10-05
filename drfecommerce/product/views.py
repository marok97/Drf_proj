from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from drf_spectacular.utils import extend_schema
from .models import Category, Brand, Product
from .serializers import CategorySerializer, BrandSerializer, ProductSerializer

# Create your views here.


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
    queryset = Product.objects.all()

    @extend_schema(responses=ProductSerializer)
    def list(self, request):
        serializer = ProductSerializer(self.queryset, many=True)
        data = serializer.data

        return Response(data, status=status.HTTP_200_OK)

    @action(
        methods=["GET"],
        detail=False,
        url_path=r"category/(?P<category>\w+)/all",
    )
    def product_list_by_category(self, request, category=None):
        serializer = ProductSerializer(
            self.queryset.filter(category__name=category), many=True
        )
        data = serializer.data
        return Response(data, status=status.HTTP_200_OK)
