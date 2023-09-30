from django.test import TestCase
from django.contrib.auth.models import User
from .models import Book

class BookGiveawayTests(TestCase):

    def setUp(self):
        # Create a test user
        self.user = User.objects.create_user(
            username='testuser',
            password='testpassword'
        )

    def test_user_registration(self):
        # Test user registration functionality
        response = self.client.post('/register/', {
            'username': 'newuser',
            'password1': 'newpassword123',
            'password2': 'newpassword123',
            'email': 'newuser@example.com'
        })
        self.assertEqual(response.status_code, 302)  # Check if the registration was successful

    def test_book_creation(self):
        # Test book creation functionality
        self.client.login(username='testuser', password='testpassword')
        response = self.client.post('/create-book/', {
            'title': 'Test Book',
            'author': 1,  # Replace with a valid author ID
            'genre': 1,   # Replace with a valid genre ID
            'condition': 1,  # Replace with a valid condition ID
            'pickup_location': 'Library'
        })
        self.assertEqual(response.status_code, 200)  # Check if the book was created successfully


