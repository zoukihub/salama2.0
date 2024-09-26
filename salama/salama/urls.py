"""
URL configuration for salama project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from products import views as product_views
from django.http import HttpResponseNotFound

urlpatterns = [
    path('admin/', admin.site.urls),
    path('signup/', include(('accounts.urls', 'accounts'), namespace='accounts')),
    path('accounts/', include('allauth.urls')),
    path('accounts/', include('accounts.urls', namespace='accounts')),
    path('cart/', include('cart.urls', namespace='cart')),
    path('orders/', include('orders.urls', namespace='orders')),
    path('products/', include('products.urls', namespace='products')),
    path('', product_views.product_list, name='home'),

]
def custom_page_not_found_view(request, exception):
    return HttpResponseNotFound(f"The requested URL {request.path} was not found.")

handler404 = 'salama.urls.custom_page_not_found_view'

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
