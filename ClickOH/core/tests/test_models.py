from django.test import TestCase
from django.contrib.auth import get_user_model
from core import models

def sample_user(email='clickoh@test.com', password='pass1234'):
    """ Crea usuario para ejemplos """
    return get_user_model().objects.create_user(email, password)

class ModelTest(TestCase):

    def test_create_user_with_email_successful(self):
        """ Probar creando un nuevo usuario con un email correctamente"""
        email = "test@probando.com"
        password = "Testpass123"
        user = get_user_model().objects.create_user(
            email=email,
            password=password
        )

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_new_user_email_normalized(self):
        """ Testea email para nuevo usuario normalizado """
        email = 'test@PROBANDO.COM'
        password = "Testpass123"
        user = get_user_model().objects.create_user(
            email,
            password
        )

        self.assertEqual(user.email, email.lower())

    def test_new_user_invalid_email(self):
        """ Nuevo usuario email invalido """
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(None, 'Testpass1234')

    def test_create_new_superuser(self):
        """ Testea crear superusuario """
        email = 'test@probando.com'
        password = "Testpass123"
        user = get_user_model().objects.create_superuser(
            email,
            password
        )

        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)

    def test_create_product(self):
        """ Prueba crear un producto """
        product = models.Product.objects.create(
            name='Shoes',
            price=float(200.00),
            stock=100
        )

        self.assertEqual(1,1)



