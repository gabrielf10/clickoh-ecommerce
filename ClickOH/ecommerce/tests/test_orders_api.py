import datetime

from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status
from core.models import Order

from ecommerce.serializers import OrderSerializer

ORDERS_URL = reverse('ecommerce:order-list')

class PublicProductsApiTests(TestCase):
    """ Test para la API de productos pública """

    def setUp(self):
        self.client = APIClient()

    def test_login_required(self):
        """ Prueba que login sea requerido para obtener las ordenes """

        res = self.client.get(ORDERS_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateProductsApiTests(TestCase):
    """ Test para la API de ordenes privados """
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            email='clickoh@ecommerce.com',
            password='pass1234',
            name='name'
        )

        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_retrieve_orders(self):
        """ Test para obtener las ordenes """
        Order.objects.create()

        res = self.client.get(ORDERS_URL)

        orders = Order.objects.all()
        serializer = OrderSerializer(orders, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)


