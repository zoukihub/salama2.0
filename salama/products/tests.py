from django.urls import reverse
from django.test import TestCase
from.models import Category, Product
from .forms import ProductForm

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
        expected_url = f'/products/product/{self.product.id}/stethoscope/'
        self.assertEqual(self.product.name, 'Stethoscope')
        self.assertEqual(self.product.get_absolute_url(), f'/products/product/{self.product.id}/stethoscope/')
    
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
        response=self.client.get(reverse('products:product_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'products/product/list.html')
        self.assertIn(self.product, response.context['products'])

class ProductFormTest(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name='Medical Devices', slug='medical-devices')
    
    def test_valid_form(self):
        """"Test if the form is valid with correct data"""
        data = {
            'name': 'Stethoscope',
            'slug': 'stethoscope',
            'price': 99.99,
            'category': self.category.id,
            'description': 'High quality stethoscope',
            'stock': 50,
            'available': True
        }
        form = ProductForm(data=data)
        self.assertTrue(form.is_valid())
        print(form.errors)

    def test_invalid_form(self):
        """"Test if the form is invalid when required fields are missing"""
        form = ProductForm({})
        self.assertFalse(form.is_valid())
        self.assertIn('name', form.errors)

# Create your tests here.
