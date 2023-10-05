from django.urls import path, include
from .views import CategoryView, BrandView, ProductView


urlpatterns = [
    path("category/", CategoryView.as_view(), name="Category"),
    path("brand", BrandView.as_view(), name="Brand"),
    path(
        "product",
        ProductView.as_view(),
    ),
]
