from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import (
    KindListView,
    NoteViewSet,
    NoteAggregationView,
)


router = DefaultRouter()
router.register('', NoteViewSet, basename='notes')

urlpatterns = [
    #
    path('kinds/', KindListView.as_view()),
    path('aggregations/vehicles/<int:vehicle_pk>/', NoteAggregationView.as_view()),
    path('', include(router.urls)),
]
