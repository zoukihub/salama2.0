from django.shortcuts import render, get_object_or_404
from .models import Product, Category
from django.db.models import Q

def product_list(request, category_slug=None):
    category = None
    categories = Category.objects.all()
    products = Product.objects.filter(available=True)
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)
    return render(request, 'products/templates/products/list.html', {
        'category': category,
        'categories': categories,
        'products': products, 
    })
    

def product_detail(request, id, slug):
    product = get_object_or_404(Product, id=id, slug=slug, available=True)
    return render(request, 'products/templates/products/detail.html', {
        'product: product'
    })

def product_search(request):
    query = request.GET.get('q')
    products = []
    if query: 
        products = Product.objects.filter(
            Q(name__icontains=query) | Q(description__icontains=query), available=True
        )
    return render(request, 'products/templates/products/search.html', {
        'products': products,
        'query': query, 
    })

from django.shortcuts import render, redirect
from django.template import loader
from .forms import ProductForm
from .models import Product
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

def product_create(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('product_list')
        else:
            form = ProductForm()
        return render(request, 'products/templates/products/product_form.html', {'form': form})
    
def product_list(request):
    products = Product.objects.all()
    context = {'products': products}
    template = loader.get_template('products/templates/products/list.html')
    print(f"Using template: {template.template.name}")
    return render(request, 'products/templates/products/product_list.html', context)

def add_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save()
            channel_layer = get_channel_layer()
            async_to_sync(channel_layer.group_send)(
                'notifications',
                {
                    'type': 'send_notification',
                    'message': f'New product "{product.name}" added.'
                }
            )
            return redirect('products:product_list')
        else:
            form = ProductForm()
        return render(request, 'products/templates/products/add_product.html', {'form': form})

# Create your views here.
