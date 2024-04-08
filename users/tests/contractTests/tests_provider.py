from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status


class TestUserRetrievalContractProvider(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_user_retrieval_contract_provider(self):
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
        self.assertIn('id_users', user)
        self.assertIn('email', user)
        self.assertIn('fullName', user)
        self.assertIn('CEP', user)
        self.assertIn('age', user)
        self.assertIn('cellPhone', user)
        self.assertIn('address', user)
        self.assertIn('create_at', user)
        self.assertIn('update_at', user)


class TestUserUpdateContractProvider(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_user_update_contract_provider(self):
        data = {
            'email': 'test@example.com',
            'fullName': 'Test User',
            'CEP': '12345678',
            'age': 25
        }
        self.client.post('/user/', data, format='json')
        updated_data = {
            'email': 'test@example.com',
            'fullName': 'Updated Test User',
            'CEP': '87654321',
            'age': 30
        }
        response = self.client.put('/user/', updated_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        updated_user = response.data
        self.assertIn('id_users', updated_user)
        self.assertIn('email', updated_user)
        self.assertIn('fullName', updated_user)
        self.assertIn('CEP', updated_user)
        self.assertIn('age', updated_user)
        self.assertIn('cellPhone', updated_user)
        self.assertIn('address', updated_user)
        self.assertIn('create_at', updated_user)
        self.assertIn('update_at', updated_user)


class TestUserDeletionContractProvider(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_user_deletion_contract_provider(self):
        data = {
            'email': 'test@example.com',
            'fullName': 'Test User',
            'CEP': '12345678',
            'age': 25
        }
        self.client.post('/user/', data, format='json')
        data = {'email': 'test@example.com'}
        response = self.client.delete('/user/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
