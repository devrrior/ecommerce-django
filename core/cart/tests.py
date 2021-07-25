from django.test import TestCase
from core.cart.models import Order


# Create your tests here.
class OrderTests(TestCase):
    def setUp(self):
        Order.objects.create(total=-1)

    def test_new_order(self):
        order = Order.objects.all().first()
        self.assertEquals(order.total, float(-1))
