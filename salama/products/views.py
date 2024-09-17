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

    context = {
        'category': category,
        'categories': categories,
        'products': products, 
    }
    return render(request, 'products/product/list.html', context)

def product_detail(request, id, slug):
    product = get_object_or_404(Product, id=id, slug=slug, available=True)
    context = {
        'product': product
    }
    return render(request, 'products/product/detail.html', context)

def product_search(request):
    query = request.GET.get('q')
    products = []
    if query: 
        products = Product.objects.filter(
            Q(name__icontains=query) | Q(description__icontains=query), available=True
        )
    
    context = {
        'products': products,
        'query': query
    }
    return render(request, 'products/product/search.html', context)
# Create your views here.
