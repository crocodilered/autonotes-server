import os

from rest_framework import generics, viewsets
from rest_framework import status
from rest_framework.response import Response

from .serializers import (
    MakerShortSerializer,
    MakerRetrieveSerializer,
    VehicleSerializer
)
from .models import Maker, Vehicle
from .permissions import OwnerPerm


class MakerListView(generics.ListAPIView):
    queryset = Maker.objects.all()
    serializer_class = MakerShortSerializer


class MakerRetrieveView(generics.RetrieveAPIView):
    queryset = Maker.objects.all()
    serializer_class = MakerRetrieveSerializer


class VehicleViewSet(viewsets.ModelViewSet):
    queryset = Vehicle.objects.all()
    serializer_class = VehicleSerializer
    permission_classes = [OwnerPerm]
    http_method_names = ['put', 'patch', 'delete', 'post']

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
