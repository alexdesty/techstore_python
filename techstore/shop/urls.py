from django.urls import path

from shop.views import *

urlpatterns = [

    #Products
    path('api/v1/products/', ProductListAPIView.as_view()),
    path('api/v1/products/<int:pk>/', ProductDetailAPIView.as_view()),

    #Categories
    path('api/v1/categorieslist/', CategoryListAPIView.as_view()),
    path('api/v1/categorieslist/<int:pk>/', CategoryDetailAPIView.as_view()),

    #CartProducts
    path('api/v1/cartproducts/', CartProductListAPIView.as_view()),
    path('api/v1/cartproducts/<int:pk>/', CartProductDetailAPIView.as_view()),

    #Shop addresses
    path('api/v1/shopaddresses/', ShopAddressListAPIView.as_view()),
    path('api/v1/shopaddresses/<int:pk>/', ShopAddressDetailAPIView.as_view()),

    #Delivery statuses
    path('api/v1/deliverystatuses/', DeliveryStatusListAPIView.as_view()),
    path('api/v1/deliverystatuses/<int:pk>/', DeliveryStatusDetailAPIView.as_view()),

    # Orders
    path('api/v1/orders/', OrderListAPIView.as_view()),
    path('api/v1/orders/<int:pk>/', OrderDetailAPIView.as_view()),
]