from django.test import TestCase
from users.serializers import UsersSerializer
from users.models import Users
from rest_framework.parsers import JSONParser
from io import BytesIO


class UsersSerializerTest(TestCase):
    def test_serialization(self):
        user_data = {
            'email': 'test@example.com',
            'fullName': 'Test User',
            'CEP': '12345678',
            'age': 25
        }
        user = Users.objects.create(**user_data)
        serializer = UsersSerializer(instance=user)

        # Remove os campos id_users, created_at e update_at do serializer.data
        serialized_data = {key: value for key, value in serializer.data.items() if key not in ['id_users', 'create_at', 'update_at']}

        expected_data = {
            'email': 'test@example.com',
            'fullName': 'Test User',
            'CEP': '12345678',
            'age': 25,
            'cellPhone': None,
            'address': None,
        }
        self.assertEqual(serialized_data, expected_data)

    def test_deserialization(self):
        """Verifica se os dados serializados em formato JSON são desserializados corretamente para instâncias do modelo Users."""
        serialized_data = '{"email": "test@example.com", "fullName": "Test User", "CEP": "12345678", "age": 25}'
        stream = BytesIO(serialized_data.encode('utf-8'))
        data = JSONParser().parse(stream)
        serializer = UsersSerializer(data=data)
        self.assertTrue(serializer.is_valid())
        instance = serializer.save()
        self.assertIsInstance(instance, Users)
        self.assertEqual(instance.email, 'test@example.com')
        self.assertEqual(instance.fullName, 'Test User')
        self.assertEqual(instance.CEP, '12345678')
        self.assertEqual(instance.age, 25)
