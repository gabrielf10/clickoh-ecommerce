from django.urls import path, include
from rest_framework.routers import DefaultRouter

from ecommerce import views

router = DefaultRouter()
router.register('products', views.ProductViewSet)
router.register('orders', views.OrderViewSet)
router.register('order-details', views.OrderDetailViewSet)


app_name = 'ecommerce'

urlpatterns = [
    path('', include(router.urls))
]


