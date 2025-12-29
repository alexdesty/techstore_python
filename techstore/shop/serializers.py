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

    def create(self, validated_data):
        return Product.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.price = validated_data.get('price', instance.price)
        instance.photo = validated_data.get('photo', instance.photo)
        instance.description = validated_data.get('description', instance.description)
        instance.category_id = validated_data.get('category_id', instance.category_id)
        instance.save()
        return instance


class CategorySerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(max_length=150)

    def create(self, validated_data):
        return Category.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.save()
        return instance


class CartSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    user_id = serializers.IntegerField(read_only=True)
    isPurchase = serializers.BooleanField()

    def create(self, validated_data):
        return Cart.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.isPurchase = validated_data.get('isPurchase', instance.isPurchase)
        instance.save()
        return instance


class CartProductSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    amount = serializers.IntegerField()
    product_id = serializers.IntegerField()
    cart_id = serializers.IntegerField(read_only=True)

    def create(self, validated_data):
        return CartProduct.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.amount = validated_data.get('amount', instance.amount)
        instance.product_id = validated_data.get('product_id', instance.product_id)
        instance.save()
        return instance


class ShopAddressSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    address = serializers.CharField(max_length=150)

    def create(self, validated_data):
        return ShopAddress.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.address = validated_data.get('address', instance.address)
        instance.save()
        return instance


class DeliveryStatusSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(max_length=150)

    def create(self, validated_data):
        return DeliveryStatus.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.save()
        return instance


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
        if deliveryType == 1 and deliveryAddress is not None:
            raise serializers.ValidationError("deliveryAddress must be Null if deliveryType is True")
        if deliveryType == 1 and shopAddress is None:
            raise serializers.ValidationError("shopAddress can't be Null if deliveryType is True")
        if deliveryAddress is not None and deliveryType == 0:
            raise serializers.ValidationError("deliveryAddress must be Null if deliveryType is False")
        if deliveryAddress is not None and deliveryType == 0 and shopAddress is not None:
            raise serializers.ValidationError("shopAddress must be Null if deliveryType is False")
        if shopAddress is not None and deliveryType == 0:
            raise serializers.ValidationError("shopAddress must be Null if deliveryType is False")
        if shopAddress is None and deliveryType == 0:
            raise serializers.ValidationError("shopAddress can't be null if deliveryType is False")
        return value

    def validate_deliveryPhoneNumber(self, value):
        pattern = r"^(80|\+375)[ -]?(\(\d{2}\)|\d{2})[ -]?\d{3}[ -]?\d{2}[ -]?\d{2}$"
        if re.fullmatch(pattern, value):
            return value
        else:
            raise serializers.ValidationError("Phone number must be entered in the format: +375299999999 or 80299999999")

    def create(self, validated_data):
        return Order.objects.create(**validated_data)


class OrderEditSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    deliveryAddress = serializers.CharField(max_length=150, required=False)
    deliveryType = serializers.BooleanField(required=True)
    deliveryPhoneNumber = serializers.CharField(max_length=20, required=False)
    user_id = serializers.IntegerField(read_only=True)
    shopAddress_id = serializers.IntegerField(required=False)
    deliveryStatus_id = serializers.IntegerField()
    cart_id = serializers.IntegerField(read_only=True)
    date = serializers.DateTimeField(read_only=True, format='%Y-%m-%d %H:%M:%S')

    def validate(self, value):
        deliveryAddress = value.get('deliveryAddress')
        deliveryType = value.get('deliveryType')
        shopAddress = value.get('shopAddress_id')
        if deliveryType == 1 and deliveryAddress is not None:
            raise serializers.ValidationError("deliveryAddress must be Null if deliveryType is True")
        if deliveryType == 1 and shopAddress is None:
            raise serializers.ValidationError("shopAddress can't be Null if deliveryType is True")
        if deliveryAddress is not None and deliveryType == 0:
            raise serializers.ValidationError("deliveryAddress must be Null if deliveryType is False")
        if deliveryAddress is not None and deliveryType == 0 and shopAddress is not None:
            raise serializers.ValidationError("shopAddress must be Null if deliveryType is False")
        if shopAddress is not None and deliveryType == 0:
            raise serializers.ValidationError("shopAddress must be Null if deliveryType is False")
        if shopAddress is None and deliveryType == 0:
            raise serializers.ValidationError("shopAddress can't be null if deliveryType is False")
        return value

    def validate_deliveryPhoneNumber(self, value):
        pattern = r"^(80|\+375)[ -]?(\(\d{2}\)|\d{2})[ -]?\d{3}[ -]?\d{2}[ -]?\d{2}$"
        if re.fullmatch(pattern, value):
            return value
        else:
            raise serializers.ValidationError(
                "Phone number must be entered in the format: +375299999999 or 80299999999")

    def update(self, instance, validated_data):
        instance.deliveryAddress = validated_data.get('deliveryAddress', instance.deliveryAddress)
        instance.deliveryType = validated_data.get('deliveryType', instance.deliveryType)
        instance.deliveryStatus_id = validated_data.get('deliveryStatus_id', instance.deliveryStatus_id)
        instance.deliveryType = validated_data.get('deliveryType', instance.deliveryType)
        instance.deliveryPhoneNumber = validated_data.get('deliveryPhoneNumber', instance.deliveryPhoneNumber)
        instance.shopAddress_id = validated_data.get('shopAddress_id', instance.shopAddress_id)
        instance.save()
        return instance


