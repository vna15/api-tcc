from django.test import TestCase
from ...models import Users
from django.db.utils import IntegrityError
from django.utils import timezone
import time


class UsersModelTest(TestCase):

    def test_object_creation(self):
        """Verifica se um objeto Users pode ser criado corretamente."""
        user = Users.objects.create(
            email="test@example.com",
            fullName="Test User",
            CEP="12345678",
            age=25,
            cellPhone="12345678901",
            address="123 Test St"
        )
        self.assertEqual(user.email, "test@example.com")
        self.assertEqual(user.fullName, "Test User")
        self.assertEqual(user.CEP, "12345678")
        self.assertEqual(user.age, 25)
        self.assertEqual(user.cellPhone, "12345678901")
        self.assertEqual(user.address, "123 Test St")

    def test_auto_now_add(self):
        """Verifica se a data de criação é definida automaticamente."""
        user = Users.objects.create(email="test@example.com", fullName="Test User", CEP="12345678", age=25)
        time.sleep(0.5)
        self.assertTrue(user.create_at < timezone.now())

    def test_auto_now(self):
        """Verifica se a data de atualização é atualizada automaticamente."""
        user = Users.objects.create(email="test1@example.com", fullName="Test User", CEP="12345678", age=25)
        original_update_at = user.update_at
        time.sleep(0.5)
        user.fullName = "Updated User"
        user.save()
        self.assertNotEqual(user.update_at, original_update_at)

    def test_unique_email(self):
        """Verifica se o campo de e-mail é único."""
        Users.objects.create(email="test2@example.com", fullName="Test User", CEP="12345678", age=25)
        with self.assertRaises(IntegrityError):
            Users.objects.create(email="test2@example.com", fullName="Another User", CEP="87654321", age=30)

    def test_optional_fields_required(self):
        """Verifica se os campos opcionais podem ser deixados em branco."""
        user = Users.objects.create(email="test4@example.com", fullName="Test User", CEP="12345678", age=25)
        self.assertIsNone(user.cellPhone)
        self.assertIsNone(user.address)

    def test_max_length_email(self):
        """Verifica se o campo de e-mail aceita um valor no tamanho máximo permitido."""
        user = Users.objects.create(email="a" * 100 + "@example.com", fullName="Test User", CEP="12345678", age=25)
        self.assertEqual(user.email, "a" * 100 + "@example.com")

    def test_max_length_fullName(self):
        """Verifica se o campo de nome completo aceita um valor no tamanho máximo permitido."""
        user = Users.objects.create(email="test5@example.com", fullName="a" * 100, CEP="12345678", age=25)
        self.assertEqual(user.fullName, "a" * 100)

    def test_CEP_length(self):
        """Verifica se o campo de CEP aceita exatamente 8 caracteres."""
        # Tenta criar um objeto Users com um CEP de 8 caracteres
        user = Users.objects.create(email="test20@example.com", fullName="Test User", CEP="12345678", age=25)

        # Verifica se o objeto foi criado com sucesso
        self.assertEqual(user.CEP, "12345678")

    def test_max_length_cellPhone(self):
        """Verifica se o campo de número de telefone aceita um valor no tamanho máximo permitido."""
        user = Users.objects.create(email="test9@example.com", fullName="Test User", CEP="12345678", age=25, cellPhone="1" * 11)
        self.assertEqual(user.cellPhone, "1" * 11)

    def test_max_length_address(self):
        """Verifica se o campo de endereço aceita um valor no tamanho máximo permitido."""
        user = Users.objects.create(email="test11@example.com", fullName="Test User", CEP="12345678", age=25, address="a" * 100)
        self.assertEqual(user.address, "a" * 100)

    def test_age_positive_integer(self):
        """Verifica se o campo de idade aceita apenas números inteiros positivos."""
        with self.assertRaises(IntegrityError):
            Users.objects.create(email="test17@example.com", fullName="Test User", CEP="12345678", age=-25)

    def test_unique_id_users(self):
        """Verifica se cada ID de usuário gerado é único."""
        user1 = Users.objects.create(email="test15@example.com", fullName="Test User", CEP="12345678", age=25)
        user2 = Users.objects.create(email="test16@example.com", fullName="Another User", CEP="87654321", age=30)
        self.assertNotEqual(user1.id_users, user2.id_users)
