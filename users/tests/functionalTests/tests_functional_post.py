from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from ...models import Users


class UserFunctionalTests(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_create_user(self):
        data = {
            "email": "test@example.com",
            "fullName": "John Doe",
            "CEP": "12345678",
            "age": 30
        }
        response = self.client.post('/user/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Users.objects.count(), 1)
        self.assertEqual(Users.objects.get().email, 'test@example.com')
        user = Users.objects.first()
        self.assertEqual(user.email, data["email"])
        self.assertEqual(user.fullName, data["fullName"])
        self.assertEqual(user.CEP, data["CEP"])
        self.assertEqual(user.age, data["age"])

    def test_duplicate_email(self):
        Users.objects.create(email="test@example.com", fullName="John Doe", CEP="12345678", age=30)
        data = {
            "email": "test@example.com",
            "fullName": "Jane Doe",
            "CEP": "87654321",
            "age": 25
        }
        response = self.client.post('/user/', data, format='json')
        self.assertIn(response.status_code, [status.HTTP_400_BAD_REQUEST, status.HTTP_409_CONFLICT])

    def test_missing_required_fields(self):
        data = {
            "email": "test@example.com",
            # Missing fullName, CEP, and age
        }
        response = self.client.post('/user/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_invalid_email_length(self):
        data = {
            "email": "a" * 101 + "@example.com",  # Exceeds maximum length
            "fullName": "John Doe",
            "CEP": "12345678",
            "age": 30
        }
        response = self.client.post('/user/', data, format='json')
        self.assertIn(response.status_code, [status.HTTP_400_BAD_REQUEST, status.HTTP_422_UNPROCESSABLE_ENTITY])

    def test_invalid_fullname_length(self):
        data = {
            "email": "test@example.com",
            "fullName": "a" * 101,  # Exceeds maximum length
            "CEP": "12345678",
            "age": 30
        }
        response = self.client.post('/user/', data, format='json')
        self.assertIn(response.status_code, [status.HTTP_400_BAD_REQUEST, status.HTTP_422_UNPROCESSABLE_ENTITY])

    def test_invalid_CEP_length(self):
        data = {
            "email": "test@example.com",
            "fullName": "John Doe",
            "CEP": "123456789",  # Exceeds maximum length
            "age": 30
        }
        response = self.client.post('/user/', data, format='json')
        self.assertIn(response.status_code, [status.HTTP_400_BAD_REQUEST, status.HTTP_422_UNPROCESSABLE_ENTITY])

    def test_invalid_phone_length(self):
        data = {
            "email": "test@example.com",
            "fullName": "John Doe",
            "CEP": "12345678",
            "age": 30,
            "cellPhone": "1" * 21  # Exceeds maximum length
        }
        response = self.client.post('/user/', data, format='json')
        self.assertIn(response.status_code, [status.HTTP_400_BAD_REQUEST, status.HTTP_422_UNPROCESSABLE_ENTITY])

    def test_invalid_age(self):
        data = {
            "email": "test@example.com",
            "fullName": "John Doe",
            "CEP": "12345678",
            "age": -20  # Negative value
        }
        response = self.client.post('/user/', data, format='json')
        self.assertIn(response.status_code, [status.HTTP_400_BAD_REQUEST, status.HTTP_422_UNPROCESSABLE_ENTITY])

    def test_existing_email(self):
        Users.objects.create(email="test@example.com", fullName="John Doe", CEP="12345678", age=30)
        data = {
            "email": "test@example.com",
            "fullName": "Jane Doe",
            "CEP": "87654321",
            "age": 25
        }
        response = self.client.post('/user/', data, format='json')
        self.assertIn(response.status_code, [status.HTTP_400_BAD_REQUEST, status.HTTP_409_CONFLICT])

    def test_successful_creation(self):
        data = {
            "email": "test@example.com",
            "fullName": "John Doe",
            "CEP": "12345678",
            "age": 30
        }
        response = self.client.post('/user/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Users.objects.count(), 1)
        user = Users.objects.first()
        self.assertEqual(user.email, data["email"])
        self.assertEqual(user.fullName, data["fullName"])
        self.assertEqual(user.CEP, data["CEP"])
        self.assertEqual(user.age, data["age"])
