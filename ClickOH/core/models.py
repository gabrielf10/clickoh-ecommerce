from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin


class UserManager(BaseUserManager):

    def create_user(self, email, password=None, **extra_fields):
        """ Crea y guarda un nuevo usuario """
        if not email:
            raise ValueError("User must have an email.")

        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password):
        """ Crea y guarda un nuevo super usuario """

        user = self.create_user(email, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)

        return user


class User(AbstractBaseUser, PermissionsMixin):
    """ Modelo personalizado de usuario que soporta hacer login con email en vez de usuario """
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'


class Product(models.Model):
    """ Modelo de Productos """
    name = models.CharField(max_length=255)
    price = models.FloatField()
    stock = models.IntegerField()

    def __str__(self):
        return self.name

    def product_with_stock(self):
        if self.stock == 0:
            return False
        return True


class Order(models.Model):
    """ Modelo de ordenes de compra """
    date_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.date_time)


class OrderDetail(models.Model):
    """ Tabla intermedia detalles de la orden"""
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    cuantity = models.IntegerField()
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.cuantity} products of {self.product.name}"

    def get_total(self):
        return self.cuantity * self.product.price
