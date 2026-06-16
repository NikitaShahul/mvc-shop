from django.test import TestCase

from shop.models import Customer, Product, Purchase


class CustomerModelTests(TestCase):
    def setUp(self):
        self.product = Product.objects.create(name="Швабра", price=1000)
        self.customer = Customer.objects.create(name="Иванов")

    def test_initial_discount_is_zero(self):
        self.assertEqual(self.customer.discount_percent, 0)

    def test_register_purchase_creates_record(self):
        purchase = self.customer.register_purchase(self.product)
        self.assertEqual(Purchase.objects.count(), 1)
        self.assertEqual(purchase.discount_percent, 0)
        self.assertEqual(purchase.price_paid, 1000)
        self.assertEqual(self.customer.purchase_count, 1)

    def test_cumulative_discount_grows(self):
        for _ in range(5):
            self.customer.register_purchase(self.product)
        self.assertEqual(self.customer.purchase_count, 5)
        self.assertEqual(self.customer.discount_percent, 5)
        purchase = self.customer.register_purchase(self.product)
        self.assertEqual(purchase.discount_percent, 5)
        self.assertEqual(purchase.price_paid, 950)

    def test_discount_reaches_max(self):
        self.customer.purchase_count = 20
        self.customer.save()
        self.assertEqual(self.customer.discount_percent, 15)
