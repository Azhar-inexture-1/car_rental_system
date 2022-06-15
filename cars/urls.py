from django.urls import path
from .views import (
    ListCreateTypeAPIView,
    TypeRetrieveUpdateDestroyAPIView,
    ListCreateBrandAPIView,
    BrandRetrieveUpdateDestroyAPIView,
    ListCreateCarAPIView,
    CarRetrieveUpdateDestroyAPIView,
)

urlpatterns = [
    path('list_create_type/', ListCreateTypeAPIView.as_view(), name='list-create-car-type'),
    path('<int:pk>/type_detail/', TypeRetrieveUpdateDestroyAPIView.as_view(), name='car-type-detail'),

    path('list_create_brand/', ListCreateBrandAPIView.as_view(), name='list-create-car-brand'),
    path('<int:pk>/brand_detail/', BrandRetrieveUpdateDestroyAPIView.as_view(), name='car-brand-detail'),

    path('list_create_car/', ListCreateCarAPIView.as_view(), name='list-create-car'),
    path('<int:pk>/car_detail/', CarRetrieveUpdateDestroyAPIView.as_view(), name='car-detail'),
]
