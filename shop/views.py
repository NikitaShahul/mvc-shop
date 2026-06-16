from django.shortcuts import get_object_or_404, render

from .models import Customer, Product


def index(request):
    """Главная страница: список товаров и покупателей."""
    products = Product.objects.all()
    customers = Customer.objects.all().order_by("name")
    context = {"products": products, "customers": customers}
    return render(request, "shop/index.html", context)


def buy(request, product_id):
    """Покупка товара с учётом накопительной скидки покупателя."""
    product = get_object_or_404(Product, pk=product_id)
    if request.method == "POST":
        name = (request.POST.get("customer_name") or "").strip()
        if name:
            customer, _ = Customer.objects.get_or_create(name=name)
            purchase = customer.register_purchase(product)
            context = {
                "product": product,
                "customer": customer,
                "purchase": purchase,
                "next_discount": customer.discount_percent,
            }
            return render(request, "shop/purchase_done.html", context)
    return render(request, "shop/buy.html", {"product": product})


def customer_detail(request, customer_id):
    """Карточка покупателя: история покупок и текущая скидка."""
    customer = get_object_or_404(Customer, pk=customer_id)
    purchases = customer.purchase_set.all().order_by("-date")
    context = {"customer": customer, "purchases": purchases}
    return render(request, "shop/customer_detail.html", context)
