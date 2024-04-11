from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from ...models import Users
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import AccessToken


class TestUsersViews(TestCase):
    def setUp(self):
        self.client = APIClient()

        # Cria um usuário de teste
        self.user = User.objects.create_user(username='testuser', password='12345')

        # Cria um token JWT para o usuário
        self.token = AccessToken.for_user(self.user)

        # Configura a autenticação com o token JWT nos headers do cliente
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')

    def test_create_user(self):
        # Teste de criação de usuário com dados válidos
        data = {
            'email': 'test@example.com',
            'fullName': 'Test User',
            'CEP': '12345678',
            'age': 25
        }
        response = self.client.post('/user/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Teste de criação de usuário com e-mail já existente
        response = self.client.post('/user/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_get_user(self):
        # Cria um usuário para o teste
        user = Users.objects.create(email='test@example.com', fullName='Test User', CEP='12345678', age=25)

        # Teste de recuperação de usuário existente
        response = self.client.get('/user/?email=test@example.com', format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Teste de recuperação de usuário inexistente
        response = self.client.get('/user/?email=nonexistent@example.com', format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_user(self):
        # Cria um usuário para o teste
        user = Users.objects.create(email='test1@example.com', fullName='Test User', CEP='12345678', age=25)

        # Teste de atualização de usuário existente
        data = {
            'email': 'test1@example.com',
            'fullName': 'Updated User',
            'CEP': '87654321',
            'age': 30
        }
        response = self.client.put('/user/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Teste de atualização de usuário inexistente
        data = {
            'email': 'nonexistent@example.com',
            'fullName': 'Updated User',
            'CEP': '87654321',
            'age': 30
        }
        response = self.client.put('/user/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_user(self):
        # Cria um usuário para o teste
        user = Users.objects.create(email='test3@example.com', fullName='Test User', CEP='12345678', age=25)

        # Teste de deleção de usuário existente
        data = {'email': 'test3@example.com'}
        response = self.client.delete('/user/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        # Teste de deleção de usuário inexistente
        data = {'email': 'nonexistent@example.com'}
        response = self.client.delete('/user/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
