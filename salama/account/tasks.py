# accounts/tasks.py
from celery import shared_task
from django.core.mail import send_mail

from salama.users.signals import User

@shared_task
def send_welcome_email(user_id):
    user = User.objects.get(id=user_id)
    send_mail(
        'Welcome to our site',
        'Thank you for signing up!',
        'from@example.com',
        [user.email],
    )
def send_order_confirmation(order_id):
    pass