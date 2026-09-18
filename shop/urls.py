from django.urls import path
from . import views

app_name = "shop"

urlpatterns = [
    path("", views.home, name="home"),
    path("birds/", views.product_list, name="product_list"),
    path("category/<str:category_slug>/", views.product_list, name="category_detail"),
    path("bird/<str:slug>/", views.product_detail, name="product_detail"),
]
