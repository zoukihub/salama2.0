from django.urls import reverse
from django.test import TestCase
from.models import Category, Product

class ProductModelTest(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name= 'Medical Devices', slug='medical-devices')
        self.product = Product.objects.create(
            category=self.category,
            name='Stethoscope',
            slug='stethoscope',
            description='High quality stethoscope.',
            price=99.99,
            stock=50,
            available=True
        )
    
    def test_product_creation(self):
        """"Test if the product is created correctly"""
        self.assertEqual(self.product.name, 'Stethoscope')
        self.assertEqual(self.product.get_absolute_url(), f'/product/{self.product.id}/stethoscope/')
    
    def test_product_stock(self):
        """"Test if the stock is correct"""
        self.assertEqual(self.product.stock, 50)

class ProductListViewTest(TestCase):
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

    def test_product_list_view(self):
        """"Test if the product list view returns the correct status code and template"""
        response=self.client.get(reverse('product_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'productsproduct/list.html')
        self.assertIn(self.product, response.context['products'])
# Create your tests here.
