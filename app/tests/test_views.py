from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.contrib.messages import get_messages
from django.contrib.auth import authenticate, login


class LoginViewTests(TestCase):
    def setUp(self):
        self.test_trainer = get_user_model().objects.create_user(
            email="madmedo73@course.com", password="mu123456", is_trainer=True
        )
        self.test_admin = get_user_model().objects.create_user(
            email="admin@admin.com", password="admin", is_admin=True
        )
        self.url = reverse('app:login') #login_url
    
    def test_login_view_invalid_email_or_password(self):
        #Test that login view shows an error for invalid credentials
        response = self.client.post(self.url, {'email': 'invalid@example.com', 'password': 'ZxZXZXZXZXZX'})
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), "Invalid email or password")
        self.assertRedirects(response, self.url)

    def test_login_view_missing_fields(self):
        #Test that login view shows an error if email or password is missing
        response = self.client.post(self.url, {'email': '', 'password': 'XzXZxzx'})
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), "Both email and password are required")
        self.assertRedirects(response, self.url)

    def test_login_view_valid_user(self):
        #Test that login view logs in a valid user
        response = self.client.post(self.url, {'email': 'madmedo73@course.com', 'password': 'mu123456'})
        self.assertRedirects(response, reverse('app:trainer-dashboard'))
        self.assertTrue('_auth_user_id' in self.client.session) 

    def test_login_view_admin_user(self):
        #Test that login view redirects an admin to the admin dashboard
        response = self.client.post(self.url, {'email': 'admin@admin.com', 'password': 'admin'})
        self.assertRedirects(response, reverse('app:admin-dashboard'))
        self.assertTrue('_auth_user_id' in self.client.session) 
