from django.urls import path

from . import views

app_name = "shop"

urlpatterns = [
    path("", views.index, name="index"),
    path("buy/<int:product_id>/", views.buy, name="buy"),
    path(
        "customer/<int:customer_id>/",
        views.customer_detail,
        name="customer_detail",
    ),
]
