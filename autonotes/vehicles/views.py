import os

from django.db.models import Count
from rest_framework import generics, viewsets
from rest_framework import status
from rest_framework.response import Response

from .serializers import (
    MakerShortSerializer,
    MakerRetrieveSerializer,
    VehicleSerializer
)
from .models import Maker, Vehicle


class MakerListView(generics.ListAPIView):
    # TODO: make in available for authed users only
    queryset = Maker.objects.all()
    serializer_class = MakerShortSerializer


class MakerRetrieveView(generics.RetrieveAPIView):
    # TODO: make in available for authed users only
    queryset = Maker.objects.all()
    serializer_class = MakerRetrieveSerializer


class VehicleViewSet(viewsets.ModelViewSet):
    serializer_class = VehicleSerializer

    def get_queryset(self):
        user = self.request.user

        if not user.is_authenticated:
            return Vehicle.objects.none()

        return Vehicle.objects\
            .filter(user=user)\
            .annotate(notes_count=Count('notes'))

    def destroy(self, request, *args, **kwargs):
        vehicle = self.get_object()
        notes_count = vehicle.notes.count()

        if notes_count == 0:
            # Delete photo file
            if vehicle.photo:
                try:
                    os.remove(vehicle.photo.file.name)
                except OSError as e:
                    print('Got error while delete file', e)
                    pass

            # Delete database data
            self.perform_destroy(vehicle)

            return Response(status=status.HTTP_204_NO_CONTENT)

        else:
            return Response(
                {
                    'message': f'Vehicle has {notes_count} notes, cannot delete it.',
                    'code': 'vehicle-has-notes'
                },
                status=status.HTTP_400_BAD_REQUEST
            )
