from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import UserProfile

admin.site.unregister(User)

class UserProfileInline(admin.StackInline):
    model = UserProfile
    can_delete = False

@admin.register(User)
class UserAdmin(BaseUserAdmin):
    inlines = (UserProfileInline, )


# Register your models here.
