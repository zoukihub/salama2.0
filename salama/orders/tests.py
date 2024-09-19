from django.test import TestCase
from django.urls import reverse
from products.models import Category, Product
from orders.models import Order

class CheckoutIntegrationTest(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name='Medical Devices', slug='medical-devices')
        self.product = Product.objects.create(
            category=self.category,
            name='Stethoscope',
            slug='stethoscope',
            description='High quality stethoscope.',
            price=99.99,
            stock=50,
            available=True
        )
    
    def test_checkout_process(self):
        """Test completing a checkout"""
        response = self.client.post(reverse('cart:cart_add'), {'product_id': self.prodcut.id, 'quantity': 1})
        response = self.client.get(reverse('checkout'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'orders/checkout.html')

# Create your tests here.
