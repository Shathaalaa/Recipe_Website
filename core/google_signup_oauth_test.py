from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from unittest import mock
from allauth.socialaccount.models import SocialAccount, SocialApp
from django.contrib.sites.models import Site

User = get_user_model()

class GoogleSignUpTests(TestCase):
    
    def setUp(self):
        self.client = Client()
        
        # Create a SocialApp for Google (required for allauth)
        # You'll need to do this in your test database
        site = Site.objects.get_current()
        social_app = SocialApp.objects.create(
            provider='google',
            name='Google',
            client_id='test-client-id',
            secret='test-secret',
        )
        social_app.sites.add(site)
        
    def test_google_login_url_exists(self):
        """Test that the Google login URL is accessible"""
        response = self.client.get(reverse('google_login'))
        # Should redirect to Google's OAuth page
        self.assertEqual(response.status_code, 200)
        self.assertTrue('accounts.google.com' in response.url)