from django.db.migrations import serializer
from django.shortcuts import get_object_or_404
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Product, Category, ShopAddress, DeliveryStatus, Order
from .serializers import *


class ProductListAPIView(APIView):
    permission_classes = (AllowAny,)
    @swagger_auto_schema(responses={200: ProductSerializer(many=True)})
    def get(self, request):
        lst = Product.objects.all()
        serializer = ProductSerializer(lst, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(request_body=ProductSerializer)
    def post(self, request):
        serializer = ProductSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        product = Product.objects.create(**serializer.validated_data)
        return Response(ProductSerializer(product).data, status=status.HTTP_201_CREATED)


class ProductDetailAPIView(APIView):
    def get(self, request, pk):
        product = get_object_or_404(Product, pk=pk)
        serializer = ProductSerializer(product)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(request_body=ProductSerializer)
    def put(self, request, pk):
        product = get_object_or_404(Product, pk=pk)
        serializer = ProductSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        product.name = data.get('name', product.name)
        product.description = data.get('description', product.description)
        product.price = data.get('price', product.price)
        product.photo = data.get('photo', product.photo)
        product.category_id = data.get('category_id', product.category_id)
        product.save()
        return Response(ProductSerializer(product).data, status=status.HTTP_200_OK)

    def delete(self, request, pk):
        product = get_object_or_404(Product, pk=pk)
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class CategoryListAPIView(APIView):
    @swagger_auto_schema(responses={200: CategorySerializer(many=True)})
    def get(self, request):
        lst = Category.objects.all()
        serializer = CategorySerializer(lst, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(request_body=CategorySerializer)
    def post(self, request):
        serializer = CategorySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        category = Category.objects.create(**serializer.validated_data)
        return Response(CategorySerializer(category).data, status=status.HTTP_201_CREATED)

class CategoryDetailAPIView(APIView):
    def get(self, request, pk):
        category = get_object_or_404(Category, pk=pk)
        serializer = CategorySerializer(category)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(request_body=CategorySerializer)
    def put(self, request, pk):
        category = get_object_or_404(Category, pk=pk)
        serializer = CategorySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        category.name = data.get('name', category.name)
        category.save()
        return Response(CategorySerializer(category).data, status=status.HTTP_200_OK)

    def delete(self, request, pk):
        category = get_object_or_404(Category, pk=pk)
        category.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class CartProductListAPIView(APIView):
    @swagger_auto_schema(responses={200: CartProductSerializer(many=True)})
    def get(self, request):
        active_cart = Cart.objects.filter(user=request.user, isPurchase=False).first()
        if active_cart:
            lst = CartProduct.objects.filter(cart=active_cart)
        else:
            lst = []
        serializer = CartProductSerializer(lst, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(request_body=CartProductSerializer)
    def post(self, request):
        product_id = request.data.get('product_id')
        additional_amount = int(request.data.get('amount', 1))
        cart, created = Cart.objects.get_or_create(
            user_id=request.user.id,
            isPurchase=False
        )
        cart_product, created = CartProduct.objects.get_or_create(
            cart=cart,
            product_id=product_id,
            defaults={'amount': additional_amount}
        )
        if not created:
            cart_product.amount += additional_amount
            cart_product.save()
        serializer = CartProductSerializer(cart_product)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class CartProductDetailAPIView(APIView):
    def delete(self, request, pk):
        cartProduct = get_object_or_404(CartProduct, pk=pk)
        cartProduct.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ShopAddressListAPIView(APIView):
    @swagger_auto_schema(responses={200: ShopAddressSerializer(many=True)})
    def get(self, request):
        lst = ShopAddress.objects.all()
        serializer = ShopAddressSerializer(lst, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(request_body=ShopAddressSerializer)
    def post(self, request):
        serializer = ShopAddressSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        shop_address = ShopAddress.objects.create(**serializer.validated_data)
        return Response(ShopAddressSerializer(shop_address).data, status=status.HTTP_201_CREATED)

class ShopAddressDetailAPIView(APIView):
    def get(self, request, pk):
        shopAddress = get_object_or_404(ShopAddress, pk=pk)
        serializer = ShopAddressSerializer(shopAddress)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(request_body=ShopAddressSerializer)
    def put(self, request, pk):
        shop_address = get_object_or_404(ShopAddress, pk=pk)
        serializer = ShopAddressSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        shop_address.address = serializer.validated_data.get('address', shop_address.address)
        shop_address.save()
        return Response(ShopAddressSerializer(shop_address).data, status=status.HTTP_200_OK)

    def delete(self, request, pk):
        shop_address = get_object_or_404(ShopAddress, pk=pk)
        shop_address.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class DeliveryStatusListAPIView(APIView):
    @swagger_auto_schema(responses={200: DeliveryStatusSerializer(many=True)})
    def get(self, request):
        lst = DeliveryStatus.objects.all()
        serializer = DeliveryStatusSerializer(lst, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(request_body=DeliveryStatusSerializer)
    def post(self, request):
        serializer = DeliveryStatusSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        d_status=DeliveryStatus.objects.create(**serializer.validated_data)
        return Response(DeliveryStatusSerializer(d_status).data, status=status.HTTP_201_CREATED)

class DeliveryStatusDetailAPIView(APIView):
    def get(self, request, pk):
        d_status = get_object_or_404(DeliveryStatus, pk=pk)
        serializer = DeliveryStatusSerializer(d_status)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(request_body=DeliveryStatusSerializer)
    def put(self, request, pk):
        d_status = get_object_or_404(DeliveryStatus, pk=pk)
        serializer = DeliveryStatusSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        d_status.name = serializer.validated_data.get('name', d_status.name)
        d_status.save()
        return Response(DeliveryStatusSerializer(d_status).data, status=status.HTTP_200_OK)

    def delete(self, request, pk):
        d_status = get_object_or_404(DeliveryStatus, pk=pk)
        d_status.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class OrderListAPIView(APIView):
    @swagger_auto_schema(responses={200: OrderSerializer(many=True)})
    def get(self, request):
        lst = Order.objects.filter(user_id=request.user.id)
        serializer = OrderSerializer(lst, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(request_body=OrderSerializer)
    def post(self, request):
        cart = Cart.objects.filter(user_id=request.user.id, isPurchase=False).first()
        if not cart:
            return Response({'error':"No active cart found"}, status=status.HTTP_404_NOT_FOUND)
        serializer = OrderSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        order = Order.objects.create(
            user_id=request.user.id,
            cart_id=cart.id,
            **serializer.validated_data
        )
        cart.isPurchase = True
        cart.save()
        Cart.objects.create(
            user_id=request.user.id,
            isPurchase=False
        )
        return Response(OrderSerializer(order).data, status=status.HTTP_201_CREATED)


class OrderDetailAPIView(APIView):
    def get(self, request, pk):
        order = get_object_or_404(Order, pk=pk)
        serializer = OrderSerializer(order)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk):
        order = get_object_or_404(Order, pk=pk)
        serializer = OrderSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data=serializer.validated_data
        order.deliveryAddress = data.get('deliveryAddress', order.deliveryAddress)
        order.deliveryType = data.get('deliveryType', order.deliveryType)
        order.deliveryPhoneNumber = data.get('deliveryPhoneNumber', order.deliveryPhoneNumber)
        order.shopAddress_id = data.get('shopAddress_id', order.shopAddress_id)
        order.save()
        return Response(OrderSerializer(order).data, status=status.HTTP_200_OK)

    def delete(self, request, pk):
        order = get_object_or_404(Order, pk=pk)
        order.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)