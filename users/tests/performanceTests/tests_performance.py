import pytest
import requests
from rest_framework_simplejwt.tokens import AccessToken
from django.contrib.auth.models import User

# URL da API para criar um novo usuário
API_URL = "http://localhost/user/"


# Função para obter um token de autenticação JWT
def obter_token():
    user = User.objects.create_user(username='admin', password='admin')
    token = AccessToken.for_user(user)
    return token


# Teste de desempenho para criar um novo usuário
@pytest.mark.performance
def test_criar_novo_usuario():
    # Obtém o token de autenticação
    token = obter_token()

    # Dados do novo usuário a serem enviados na requisição POST
    user_data = {
        "email": "novo_usuario@example.com",
        "fullName": "Novo Usuário",
        "CEP": "12345678",
        "age": 30
    }

    # Adiciona o token de autenticação ao cabeçalho
    headers = {"Authorization": f"Bearer {token.__str__()}"}

    # Envia a requisição POST e mede o tempo de resposta
    response = requests.post(API_URL, json=user_data, headers=headers)

    # Verifica se a requisição foi bem-sucedida
    assert response.status_code == 201

    # Imprime o tempo de resposta
    print(f"Tempo de resposta: {response.elapsed.total_seconds()} segundos")
