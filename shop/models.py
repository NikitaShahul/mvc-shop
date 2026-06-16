from django.db import models

from .discounts import apply_discount, discount_for_purchase_count


class Product(models.Model):
    """Товар магазина."""

    name = models.CharField("Наименование", max_length=200)
    price = models.PositiveIntegerField("Цена")

    def __str__(self):
        return self.name


class Customer(models.Model):
    """Покупатель с учётом количества покупок (вариант 4)."""

    name = models.CharField("Покупатель", max_length=200, unique=True)
    purchase_count = models.PositiveIntegerField("Количество покупок", default=0)

    @property
    def discount_percent(self):
        """Текущая накопительная скидка покупателя (в процентах)."""
        return discount_for_purchase_count(self.purchase_count)

    def register_purchase(self, product):
        """Зарегистрировать покупку товара и вернуть объект Purchase.

        Скидка определяется текущим количеством покупок покупателя,
        после чего счётчик покупок увеличивается на единицу.
        """
        percent = self.discount_percent
        price_paid = apply_discount(product.price, percent)
        purchase = Purchase.objects.create(
            product=product,
            customer=self,
            discount_percent=percent,
            price_paid=price_paid,
        )
        self.purchase_count += 1
        self.save(update_fields=["purchase_count"])
        return purchase

    def __str__(self):
        return self.name


class Purchase(models.Model):
    """Факт покупки товара конкретным покупателем."""

    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, verbose_name="Товар"
    )
    customer = models.ForeignKey(
        Customer, on_delete=models.CASCADE, verbose_name="Покупатель"
    )
    date = models.DateTimeField("Дата покупки", auto_now_add=True)
    discount_percent = models.PositiveIntegerField("Скидка, %", default=0)
    price_paid = models.PositiveIntegerField("Уплачено", default=0)

    def __str__(self):
        return f"{self.customer} — {self.product} ({self.price_paid})"
