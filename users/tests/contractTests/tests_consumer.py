from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status


class TestUsersEndpointAvailability(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_users_endpoint_availability(self):
        response = self.client.get('/user/')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class TestUserCreationResponseTypes(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_user_creation_response_types(self):
        data = {
            'email': 'test@example.com',
            'fullName': 'Test User',
            'CEP': '12345678',
            'age': 25
        }
        response = self.client.post('/user/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        user = response.data
        self.assertIsInstance(user['id_users'], str)
        self.assertIsInstance(user['email'], str)
        self.assertIsInstance(user['fullName'], str)
        self.assertIsInstance(user['CEP'], str)
        self.assertIsInstance(user['age'], int)
        self.assertIsInstance(user['cellPhone'], (str, type(None)))
        self.assertIsInstance(user['address'], (str, type(None)))
        self.assertIsInstance(user['create_at'], str)
        self.assertIsInstance(user['update_at'], str)


class TestUserRetrievalResponseTypes(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_user_retrieval_response_types(self):
        data = {
            'email': 'test@example.com',
            'fullName': 'Test User',
            'CEP': '12345678',
            'age': 25
        }
        self.client.post('/user/', data, format='json')
        response = self.client.get('/user/?email=test@example.com')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        user = response.data
        self.assertIsInstance(user['id_users'], str)
        self.assertIsInstance(user['email'], str)
        self.assertIsInstance(user['fullName'], str)
        self.assertIsInstance(user['CEP'], str)
        self.assertIsInstance(user['age'], int)
        self.assertIsInstance(user['cellPhone'], (str, type(None)))
        self.assertIsInstance(user['address'], (str, type(None)))
        self.assertIsInstance(user['create_at'], str)
        self.assertIsInstance(user['update_at'], str)
