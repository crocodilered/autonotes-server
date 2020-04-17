from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import MakerListView, MakerRetrieveView, VehicleViewSet


router = DefaultRouter()
router.register('', VehicleViewSet, basename='vehicles')

urlpatterns = [
    #
    path('makers/', MakerListView.as_view()),
    path('makers/<int:pk>/', MakerRetrieveView.as_view()),
    path('', include(router.urls)),
]
