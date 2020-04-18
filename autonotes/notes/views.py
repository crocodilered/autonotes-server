from django.db.models import Sum
from django.shortcuts import get_object_or_404
from django.core.exceptions import PermissionDenied
from rest_framework import generics, viewsets, views
from rest_framework import status
from rest_framework.response import Response

from .serializers import (
    KindSerializer,
    NoteSerializer, NoteListSerializer,
)

from autonotes.vehicles.models import Vehicle
from .models import Kind, Note


class KindListView(generics.ListAPIView):
    queryset = Kind.objects.all()
    serializer_class = KindSerializer


class NoteAggregationView(views.APIView):
    """ Show aggregated notes list, filtered by vehicle. """

    def get(self, request, **kwargs):
        try:
            vehicle = get_object_or_404(Vehicle, id=kwargs.get('vehicle_pk'))

            # Security action
            if vehicle.user != request.user:
                raise PermissionDenied

            notes = Note.objects\
                .filter(vehicle=vehicle)\
                .values('kind')\
                .order_by('kind')\
                .annotate(Sum('cost'))

            return Response(notes)

        except ValueError:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class NoteViewSet(viewsets.ModelViewSet):
    # TODO: clean attachments on update / delete
    def get_queryset(self):
        return Note.objects.filter(vehicle__user=self.request.user)

    def get_serializer_class(self):
        if self.action == 'list':
            return NoteListSerializer
        else:
            return NoteSerializer

    def list(self, request, *args, **kwargs):
        try:
            vehicle_id = int(request.query_params.get('vehicle'))
            kind_id = int(request.query_params.get('kind'))

            queryset = self.get_queryset().filter(vehicle__id=vehicle_id, kind__id=kind_id)
            serializer = self.get_serializer(queryset, many=True)

            return Response(serializer.data)

        except TypeError:
            return Response(
                {'message': 'Mandatory params missed: vehicle and/or kind.'},
                status=status.HTTP_400_BAD_REQUEST
            )

