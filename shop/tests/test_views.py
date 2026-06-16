from django.test import TestCase
from django.urls import reverse

from shop.models import Customer, Product, Purchase


class ViewTests(TestCase):
    def setUp(self):
        self.product = Product.objects.create(name="Ведро", price=500)

    def test_index_status_code(self):
        response = self.client.get(reverse("shop:index"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Ведро")

    def test_buy_get_shows_form(self):
        response = self.client.get(reverse("shop:buy", args=[self.product.id]))
        self.assertEqual(response.status_code, 200)

    def test_buy_post_creates_purchase(self):
        response = self.client.post(
            reverse("shop:buy", args=[self.product.id]),
            {"customer_name": "Петров"},
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Purchase.objects.count(), 1)
        customer = Customer.objects.get(name="Петров")
        self.assertEqual(customer.purchase_count, 1)

    def test_customer_detail(self):
        customer = Customer.objects.create(name="Сидоров")
        response = self.client.get(
            reverse("shop:customer_detail", args=[customer.id])
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Сидоров")
