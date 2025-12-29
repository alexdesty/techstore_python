from django.shortcuts import get_object_or_404
from drf_yasg.utils import swagger_auto_schema
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import *


class ProductListAPIView(APIView):
    permission_classes = (AllowAny,)
    @swagger_auto_schema(responses={200: ProductSerializer(many=True)})
    def get(self, request):
        lst = Product.objects.all()
        return Response({'products':ProductSerializer(lst, many=True).data})

    @swagger_auto_schema(request_body=ProductSerializer)
    def post(self, request):
        serializer = ProductSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'post':serializer.data})


class ProductDetailAPIView(APIView):
    def get(self, request, pk):
        product = get_object_or_404(Product, pk=pk)
        serializer = ProductSerializer(product)
        return Response({'product':serializer.data})

    @swagger_auto_schema(request_body=ProductSerializer)
    def put(self, request, pk):
        product = get_object_or_404(Product, pk=pk)
        serializer = ProductSerializer(instance=product, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'put': serializer.data})

    def delete(self, request, pk):
        product = get_object_or_404(Product, pk=pk)
        product.delete()
        return Response({'delete':True})


class CategoryListAPIView(APIView):
    @swagger_auto_schema(responses={200: CategorySerializer(many=True)})
    def get(self, request):
        lst = Category.objects.all()
        return Response({'categories':CategorySerializer(lst, many=True).data})

    @swagger_auto_schema(request_body=CategorySerializer)
    def post(self, request):
        serializer = CategorySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'post':serializer.data})

class CategoryDetailAPIView(APIView):
    def get(self, request, pk):
        category = get_object_or_404(Category, pk=pk)
        serializer = CategorySerializer(category)
        return Response({'category':serializer.data})

    @swagger_auto_schema(request_body=CategorySerializer)
    def put(self, request, pk):
        category = get_object_or_404(Category, pk=pk)
        serializer = CategorySerializer(instance=category, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'put': serializer.data})

    def delete(self, request, pk):
        category = get_object_or_404(Category, pk=pk)
        category.delete()
        return Response({'delete':True})


class CartProductListAPIView(APIView):
    @swagger_auto_schema(responses={200: CartProductSerializer(many=True)})
    def get(self, request):
        active_cart = Cart.objects.filter(user=request.user, isPurchase=False).first()
        if active_cart:
            lst = CartProduct.objects.filter(cart=active_cart)
        else:
            lst = []
        serializer = CartProductSerializer(lst, many=True)
        return Response({'cartproducts':serializer.data})

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
        return Response({'product':serializer.data})


class CartProductDetailAPIView(APIView):
    def delete(self, request, pk):
        cartProduct = get_object_or_404(CartProduct, pk=pk)
        cartProduct.delete()
        return Response({'delete':True})


class ShopAddressListAPIView(APIView):
    @swagger_auto_schema(responses={200: ShopAddressSerializer(many=True)})
    def get(self, request):
        lst = ShopAddress.objects.all()
        return Response({'shop_addresses':ShopAddressSerializer(lst, many=True).data})

    @swagger_auto_schema(request_body=ShopAddressSerializer)
    def post(self, request):
        serializer = ShopAddressSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'post':serializer.data})

class ShopAddressDetailAPIView(APIView):
    def get(self, request, pk):
        shopAddress = get_object_or_404(ShopAddress, pk=pk)
        serializer = ShopAddressSerializer(shopAddress)
        return Response({'shopaddress':serializer.data})

    @swagger_auto_schema(request_body=ShopAddressSerializer)
    def put(self, request, pk):
        shopAddress = get_object_or_404(ShopAddress, pk=pk)
        serializer = ShopAddressSerializer(instance=shopAddress, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'put': serializer.data})

    def delete(self, request, pk):
        shopAddress = get_object_or_404(ShopAddress, pk=pk)
        shopAddress.delete()
        return Response({'delete':True})


class DeliveryStatusListAPIView(APIView):
    @swagger_auto_schema(responses={200: DeliveryStatusSerializer(many=True)})
    def get(self, request):
        lst = DeliveryStatus.objects.all()
        return Response({'delivery statuses':DeliveryStatusSerializer(lst, many=True).data})

    @swagger_auto_schema(request_body=DeliveryStatusSerializer)
    def post(self, request):
        serializer = DeliveryStatusSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'post':serializer.data})

class DeliveryStatusDetailAPIView(APIView):
    def get(self, request, pk):
        deliveryStatus = get_object_or_404(DeliveryStatus, pk=pk)
        serializer = DeliveryStatusSerializer(deliveryStatus)
        return Response({'deliverystatus':serializer.data})

    @swagger_auto_schema(request_body=DeliveryStatusSerializer)
    def put(self, request, pk):
        deliveryStatus = get_object_or_404(DeliveryStatus, pk=pk)
        serializer = DeliveryStatusSerializer(instance=deliveryStatus, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'put': serializer.data})

    def delete(self, request, pk):
        deliveryStatus = get_object_or_404(DeliveryStatus, pk=pk)
        deliveryStatus.delete()
        return Response({'delete':True})


class OrderListAPIView(APIView):
    @swagger_auto_schema(responses={200: OrderSerializer(many=True)})
    def get(self, request):
        lst = Order.objects.filter(user_id=request.user.id)
        return Response({'orders':OrderSerializer(lst, many=True).data})

    @swagger_auto_schema(request_body=OrderSerializer)
    def post(self, request):
        cart = Cart.objects.filter(user_id=request.user.id, isPurchase=False).first()
        if not cart:
            return Response({'error':"No active cart found"})
        serializer = OrderSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        order = serializer.save(
            user_id=request.user.id,
            cart_id=cart.id,
            deliveryStatus_id=None
        )
        cart.isPurchase = True
        cart.save()
        Cart.objects.create(
            user_id=request.user.id,
            isPurchase=False
        )
        return Response({'post':serializer.data})


class OrderDetailAPIView(APIView):
    def get(self, request, pk):
        order = get_object_or_404(Order, pk=pk)
        serializer = OrderSerializer(order)
        return Response({'order':serializer.data})

    @swagger_auto_schema(request_body=OrderEditSerializer)
    def put(self, request, pk):
        order = get_object_or_404(Order, pk=pk)
        serializer = OrderEditSerializer(instance=order, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'put': serializer.data})

    def delete(self, request, pk):
        order = get_object_or_404(Order, pk=pk)
        order.delete()
        return Response({'delete':True})