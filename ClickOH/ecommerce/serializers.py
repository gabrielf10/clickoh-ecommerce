import requests
from rest_framework import serializers

from core import models


class ProductSerializer(serializers.ModelSerializer):
    """ Serializador para Producto """

    class Meta:
        model = models.Product
        fields = ('id', 'name', 'price', 'stock')
        read_only_fields = ('id',)


class OrderSerializer(serializers.ModelSerializer):
    """ Serializador para Ordenes """

    class Meta:
        model = models.Order
        fields = ('id', 'date_time')
        read_only_fields = ('id',)


class OrderDetailSerializer(serializers.ModelSerializer):
    """ Serializador para los detalles de las órdenes """

    total = serializers.SerializerMethodField('_get_total')
    total_usd = serializers.SerializerMethodField('_get_total_usd')

    def _get_total(self, order_detail_object):
        cuantity = getattr(order_detail_object, "cuantity")
        product = getattr(order_detail_object, "product")
        return round(cuantity * product.price, 2)

    def _get_total_usd(self, order_detail_object):
        cuantity = getattr(order_detail_object, "cuantity")
        product = getattr(order_detail_object, "product")

        response = requests.get('https://www.dolarsi.com/api/api.php?type=valoresprincipales')
        data_dolarsi = response.json()

        index = next((index for (index, d) in enumerate(data_dolarsi) if d["casa"]["nombre"] == "Dolar Blue"), None)

        dolar_blue = data_dolarsi[index]['casa']['compra']

        return round(cuantity * product.price / float(dolar_blue.replace(',', '.')), 2)

    class Meta:
        model = models.OrderDetail
        fields = ('id', 'order', 'product', 'cuantity', 'total', 'total_usd')
        read_only_fields = ('id',)
