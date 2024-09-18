from django.shortcuts import render, redirect, get_object_or_404
from .models import Order, OrderItem
from cart.cart import Cart
from .forms import OrderCreateForm
from django.contrib.auth.decorators import login_required
import stripe
from django.conf import settings

stripe.api_key = settings.STRIPE_SECRET_KEY

@login_required
def order_create(request):
    cart = Cart(request)
    if len(cart) == 0:
        return redirect('products:product_list')
    
    if request.method == 'POST':
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.user = request.user
            order.save()
            for item in cart:
                OrderItem.objects.create(
                    order=order,
                    product=item['product'],
                    price=item['price'],
                    quantity=item['quantity']
                )
            cart.clear()
            return redirect('orders:payment', order.id)
    else:
        form = OrderCreateForm()
    return render(request, 'orders/order_create.html', {'cart': cart, 'form': form})

@login_required
def payment(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user, paid=False)
    if request.method == 'POST':
        token = request.POST.get('stripeToken')
        try:
            charge = stripe.Charge.create(
                amount=int(order.get_total_cost() * 100),
                currency='usd',
                description=f'Order {order.id}',
                source=token,
            )
            order.paid = True
            order.save()
            return redirect('orders:payment_success')
        except stripe.error.CardError:
            return redirect('orders:payment_cancel')
    else:
        stripe_pub_key = settings.STRIPE_PUBLISHABLE_KEY
        return render(request, 'orders/payment.html', {'order': order, 'stripe_pub_key': stripe_pub_key})
    
def payment_success(request):
    return render(request, 'orders/payment_success.html')

def payment_cancel(request):
    return render(request, 'orders/payment_cancel.html')


def order_list(request):
    return render(request, 'orders/order_list.html')

# Create your views here.
