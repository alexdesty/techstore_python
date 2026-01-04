import re

from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from shop.models import *


class ProductSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(max_length=150, validators=[UniqueValidator(queryset=Product.objects.all())])
    price = serializers.DecimalField(max_digits=10, decimal_places=2)
    photo = serializers.ImageField(allow_null=True, required=False)
    description = serializers.CharField()
    category_id = serializers.IntegerField()


class CategorySerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(max_length=150)


class CartSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    user_id = serializers.IntegerField(read_only=True)
    isPurchase = serializers.BooleanField()


class CartProductSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    amount = serializers.IntegerField()
    product_id = serializers.IntegerField()
    cart_id = serializers.IntegerField(read_only=True)


class ShopAddressSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    address = serializers.CharField(max_length=150)


class DeliveryStatusSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(max_length=150)


class OrderSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    deliveryAddress = serializers.CharField(max_length=150, required=False)
    deliveryType = serializers.BooleanField(required=True)
    deliveryPhoneNumber = serializers.CharField(max_length=20, required=False)
    user_id = serializers.IntegerField(read_only=True)
    shopAddress_id = serializers.IntegerField(required=False)
    deliveryStatus_id = serializers.IntegerField(read_only=True)
    cart_id = serializers.IntegerField(read_only=True)
    date = serializers.DateTimeField(read_only=True, format='%Y-%m-%d %H:%M:%S')

    def validate(self, value):
        deliveryAddress = value.get('deliveryAddress')
        deliveryType = value.get('deliveryType')
        shopAddress = value.get('shopAddress_id')
        # 1 = delivery to shop, 0 - delivery to client address
        if deliveryType == 1 and deliveryAddress is not None:
            raise serializers.ValidationError("deliveryAddress must be Null if deliveryType is True")
        if deliveryType == 1 and shopAddress is None:
            raise serializers.ValidationError("shopAddress can't be Null if deliveryType is True")
        if deliveryAddress is None and deliveryType == 0:
            raise serializers.ValidationError("deliveryAddress can't be Null if deliveryType is False")
        if deliveryAddress is not None and deliveryType == 0 and shopAddress is not None:
            raise serializers.ValidationError("shopAddress must be Null if deliveryType is False")
        if shopAddress is not None and deliveryType == 0:
            raise serializers.ValidationError("shopAddress must be Null if deliveryType is False")
        if shopAddress is None and deliveryType == 1:
            raise serializers.ValidationError("shopAddress can't be null if deliveryType is True")
        return value

    def validate_deliveryPhoneNumber(self, value):
        pattern = r"^(80|\+375)[ -]?(\(\d{2}\)|\d{2})[ -]?\d{3}[ -]?\d{2}[ -]?\d{2}$"
        if re.fullmatch(pattern, value):
            return value
        else:
            raise serializers.ValidationError("Phone number must be entered in the format: +375299999999 or 80299999999")



