from django.test import SimpleTestCase

from shop.discounts import apply_discount, discount_for_purchase_count


class DiscountLogicTests(SimpleTestCase):
    def test_no_discount_for_new_customer(self):
        self.assertEqual(discount_for_purchase_count(0), 0)
        self.assertEqual(discount_for_purchase_count(4), 0)

    def test_tier_5_percent(self):
        self.assertEqual(discount_for_purchase_count(5), 5)
        self.assertEqual(discount_for_purchase_count(9), 5)

    def test_tier_10_percent(self):
        self.assertEqual(discount_for_purchase_count(10), 10)
        self.assertEqual(discount_for_purchase_count(19), 10)

    def test_tier_15_percent_cap(self):
        self.assertEqual(discount_for_purchase_count(20), 15)
        self.assertEqual(discount_for_purchase_count(1000), 15)

    def test_negative_count_raises(self):
        with self.assertRaises(ValueError):
            discount_for_purchase_count(-1)

    def test_apply_discount(self):
        self.assertEqual(apply_discount(1000, 0), 1000)
        self.assertEqual(apply_discount(1000, 10), 900)
        self.assertEqual(apply_discount(2500, 15), 2125)

    def test_apply_discount_invalid(self):
        with self.assertRaises(ValueError):
            apply_discount(-1, 10)
        with self.assertRaises(ValueError):
            apply_discount(100, 150)
