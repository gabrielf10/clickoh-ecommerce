from rest_framework import viewsets, mixins, status
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from core import models

from ecommerce import serializers


class BaseViewSet(viewsets.GenericViewSet, mixins.ListModelMixin, mixins.CreateModelMixin):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        """ Retorna objetos """
        return self.queryset

    def perform_create(self, serializer):
        """ Crear un nuevo objeto """
        serializer.save()


class ProductViewSet(BaseViewSet):
    """ Manejar Productos en base de datos """
    queryset = models.Product.objects.all()
    serializer_class = serializers.ProductSerializer


class OrderViewSet(BaseViewSet):
    """ Manejar Ordenes en base de datos """
    queryset = models.Order.objects.all()
    serializer_class = serializers.OrderSerializer


class OrderDetailViewSet(viewsets.ModelViewSet):
    """ Manejar Ordenes en base de datos """
    serializer_class = serializers.OrderDetailSerializer
    queryset = models.OrderDetail.objects.all()

    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        """ Retorna objetos """
        return self.queryset

    def create(self, request, *args, **kwargs):
        """ Crear un nuevo detalle de orden """
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            order = serializer.validated_data.get('order')
            product = serializer.validated_data.get('product')
            cuantity = serializer.validated_data.get('cuantity')

            product.stock -= cuantity

            if product.stock < 0:
                raise ValueError('Error when creating order, there is no stock of the product')

            product_get = models.Product.objects.get(
                id=product.pk
            )
            product_get.stock = product.stock
            product_get.save()

            order_detail = models.OrderDetail.objects.create(
                order=order,
                cuantity=cuantity,
                product=product
            )

            order_detail.save()

            serializer = serializers.OrderDetailSerializer(order_detail)
            return Response(serializer.data)
        else:
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )
