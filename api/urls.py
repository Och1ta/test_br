from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import HouseViewSet, ApartmentViewSet, ResidentViewSet, ParkingSpotViewSet, CarViewSet

router = DefaultRouter()

router.register(r'houses', HouseViewSet, basename='house')

house_residents_list = ResidentViewSet.as_view({
    'get': 'list',
    'post': 'create'
})
house_residents_detail = ResidentViewSet.as_view({
    'get': 'retrieve',
    'put': 'update',
    'patch': 'partial_update',
    'delete': 'destroy'
})
house_apartments_list = ApartmentViewSet.as_view({
    'get': 'list',
    'post': 'create'
})
house_apartments_detail = ApartmentViewSet.as_view({
    'get': 'retrieve',
    'put': 'update',
    'patch': 'partial_update',
    'delete': 'destroy'
})
house_parkingspots_list = ParkingSpotViewSet.as_view({
    'get': 'list',
    'post': 'create'
})
house_parkingspots_detail = ParkingSpotViewSet.as_view({
    'get': 'retrieve',
    'put': 'update',
    'patch': 'partial_update',
    'delete': 'destroy'
})
house_car_list = CarViewSet.as_view({
    'get': 'list',
    'post': 'create'
})
house_car_detail = CarViewSet.as_view({
    'get': 'retrieve',
    'put': 'update',
    'patch': 'partial_update',
    'delete': 'destroy'
})

urlpatterns = [
    path('', include(router.urls)),
    path('houses/<int:house_pk>/residents/', house_residents_list, name='resident-list'),
    path('houses/<int:house_pk>/residents/<int:pk>/', house_residents_detail, name='resident-detail'),
    path('houses/<int:house_pk>/apartments/', house_apartments_list, name='apartment-list'),
    path('houses/<int:house_pk>/apartments/<int:pk>/', house_apartments_detail, name='apartment-detail'),
    path('houses/<int:house_pk>/parkingspots/', house_parkingspots_list, name='parkingspot-list'),
    path('houses/<int:house_pk>/parkingspots/<int:pk>/', house_parkingspots_detail, name='parkingspot-detail'),
    path('houses/<int:house_pk>/cars/', house_car_list, name='car-list'),
    path('houses/<int:house_pk>/cars/<int:pk>/', house_car_detail, name='car-detail'),
]
