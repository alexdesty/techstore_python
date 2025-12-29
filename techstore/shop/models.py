from django.contrib.auth.models import User
from django.db import models
from django.db.models import PROTECT


class Product(models.Model):
    name = models.CharField(max_length=150, verbose_name='Наименование')
    price = models.DecimalField(verbose_name='Цена', max_digits=10, decimal_places=2)
    photo = models.ImageField(upload_to='products/', null=True, blank=True, verbose_name='Фото')
    description = models.TextField(blank=True, verbose_name='Описание')
    category = models.ForeignKey('Category', on_delete=models.CASCADE, verbose_name='Категория')
    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=150, verbose_name='Наименование')
    def __str__(self):
        return self.name


class Cart(models.Model):
    isPurchase = models.BooleanField(verbose_name='Куплена', default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь')


class ShopAddress(models.Model):
    address = models.CharField(max_length=150, verbose_name='Адрес')


class DeliveryStatus(models.Model):
    name = models.CharField(max_length=150, verbose_name='Наименование')


class Order(models.Model):
    deliveryAddress = models.CharField(max_length=150, blank=True, verbose_name='Адрес доставки', null=True)
    deliveryType = models.BooleanField(default=True, verbose_name='Тип')
    deliveryPhoneNumber = models.CharField(max_length=20, blank=True, verbose_name='Номер телефона', null = True)
    date = models.DateTimeField(auto_now_add=True, verbose_name='Дата и время')
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, verbose_name='Корзина')
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь')
    shopAddress = models.ForeignKey(ShopAddress, on_delete=models.PROTECT, verbose_name='Адрес пункта выдачи', blank=True, null=True)
    deliveryStatus = models.ForeignKey(DeliveryStatus, on_delete=PROTECT, verbose_name='Статус доставки', blank=True, null=True)


class CartProduct(models.Model):
    amount = models.IntegerField(verbose_name='Количество')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='Товар')
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, verbose_name='Корзина')

