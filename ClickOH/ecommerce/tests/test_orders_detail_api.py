# import datetime
#
# from django.test import TestCase
# from django.contrib.auth import get_user_model
# from django.urls import reverse
#
# from rest_framework.test import APIClient
# from rest_framework import status
# from core.models import Order, Product, OrderDetail
#
# from ecommerce.serializers import OrderSerializer
#
# DETAIL_URL = reverse('ecommerce:order-details')
#
# class PublicOrdersDetailApiTests(TestCase):
#     """ Test para la API de órdenes pública """
#
#     def setUp(self):
#         self.client = APIClient()
#
#     def test_login_required(self):
#         """ Prueba que login sea requerido para obtener los detalles de las órdenes """
#
#         res = self.client.get(DETAIL_URL)
#
#         self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)
#
#
# class PrivateOrdersDetailApiTests(TestCase):
#     """ Test para la API de los detalles de las órdenes privados """
#     def setUp(self):
#         self.user = get_user_model().objects.create_user(
#             email='clickoh@ecommerce.com',
#             password='pass1234',
#             name='name'
#         )
#
#         self.client = APIClient()
#         self.client.force_authenticate(user=self.user)
#
#     def test_retrieve_orders(self):
#         """ Test para obtener las órdenes """
#         OrderDetail.objects.create()
#
#         res = self.client.get(DETAIL_URL)
#
#         orders = OrderDetail.objects.all()
#         serializer = OrderSerializer(orders, many=True)
#         self.assertEqual(res.status_code, status.HTTP_200_OK)
#         self.assertEqual(res.data, serializer.data)
#
#
