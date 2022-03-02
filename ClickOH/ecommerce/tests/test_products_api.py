from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status
from core.models import Product

from ecommerce.serializers import ProductSerializer

PRODUCTS_URL = reverse('ecommerce:product-list')


class PublicProductsApiTests(TestCase):
    """ Test para la API de productos pública """

    def setUp(self):
        self.client = APIClient()

    def test_login_required(self):
        """ Prueba que login sea requerido para obtener los productos """

        res = self.client.get(PRODUCTS_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateProductsApiTests(TestCase):
    """ Test para la API de productos privados """

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            email='clickoh@ecommerce.com',
            password='pass1234',
            name='name'
        )

        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_retrieve_products(self):
        """ Test para obtener los productos """
        Product.objects.create(name='Shirt', price=11.00, stock=50)
        Product.objects.create(name='T-Shirt', price=50.00, stock=20)

        res = self.client.get(PRODUCTS_URL)

        products = Product.objects.all().order_by('-name')
        serializer = ProductSerializer(products, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        # self.assertEqual(res.data, serializer.data)

    def test_create_products(self):
        payload = {'name': 'Shirt', 'price': 11.00, 'stock': 50}
        self.client.post(PRODUCTS_URL, payload)

        exist = Product.objects.filter(
            name=payload['name']
        ).exists()

        self.assertTrue(exist)

    def test_create_product_invalid(self):
        payload = {'name': ''}
        res = self.client.post(PRODUCTS_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

class PrivateProductsApiTests(TestCase):
    """ Test para la API de productos privados """

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            email='clickoh@ecommerce.com',
            password='pass1234',
            name='name'
        )

        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_retrieve_products(self):
        """ Test para obtener los productos """
        Product.objects.create(name='Shirt', price=11.00, stock=50)
        Product.objects.create(name='T-Shirt', price=50.00, stock=20)

        res = self.client.get(PRODUCTS_URL)

        products = Product.objects.all().order_by('-name')
        serializer = ProductSerializer(products, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        # self.assertEqual(res.data, serializer.data)

    def test_create_products(self):
        payload = {'name': 'Shirt', 'price': 11.00, 'stock': 50}
        self.client.post(PRODUCTS_URL, payload)

        exist = Product.objects.filter(
            name=payload['name']
        ).exists()

        self.assertTrue(exist)

    def test_create_product_invalid(self):
        payload = {'name': ''}
        res = self.client.post(PRODUCTS_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)