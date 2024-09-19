from django.test import TestCase
from django.urls import reverse
from products.models import Category, Product
from .models import Cart

class CartIntegrationTest(TestCase):
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
    def test_add_product_to_cart(self):
        """"Test adding a product to the cart"""
        response = self.client.post(reverse('cart:cart_add'), {'product_id' : self.product.id, 'quantity': 1})
        self.assertEqual(response.status_code, 302)
        cart = self.client.session['cart']
        self.assertIn(str(self.product.id), cart)
        self.assertEqual(cart[str(self.product.id)]['quantity'], 1)
# Create your tests here.
