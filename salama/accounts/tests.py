from django.test import TestCase
from django.contrib.auth.models import User
from .models import Profile

class ProfileTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create(username='testuser')
    
    def test_profile_creation(self):
        profile = Profile.objects.get(user=self.user)
        self.assertTrue(isinstance(profile, Profile))