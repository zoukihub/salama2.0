from django.contrib.auth.models import User
from django.db import models

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    address = models.CharField(max_length=225, blank=True)
    phone = models.CharField(max_length=20, blank=True)

    def __str__(self):
        return self.user.username
# Create your models here.
