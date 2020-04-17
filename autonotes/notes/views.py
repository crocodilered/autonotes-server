from django.db.models import Sum
from rest_framework import generics, viewsets, views
from rest_framework import status
from rest_framework.response import Response

from .serializers import (
    KindSerializer,
    NoteSerializer, NoteListSerializer,
)

from .models import Kind, Note


class KindListView(generics.ListAPIView):
    # TODO: make in available for authenticated users only
    queryset = Kind.objects.all()
    serializer_class = KindSerializer


class NoteAggregationView(views.APIView):
    """ Show aggregated notes list, filtered by vehicle. """
    # TODO: implement permissions
    # permission_classes =

    def get(self, request, **kwargs):
        try:
            vehicle_id = int(kwargs.get('vehicle_pk'))

            notes = Note.objects\
                .filter(vehicle__id=vehicle_id)\
                .values('kind')\
                .order_by('kind')\
                .annotate(Sum('cost'))

            return Response(notes)

        except ValueError:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class NoteViewSet(viewsets.ModelViewSet):
    # TODO: implement permissions
    # TODO: clean attachments on update / delete
    queryset = Note.objects.all()

    def get_serializer_class(self):
        if self.action == 'list':
            return NoteListSerializer
        else:
            return NoteSerializer

    def list(self, request, *args, **kwargs):
        try:
            vehicle_id = int(request.query_params.get('vehicle'))
            kind_id = int(request.query_params.get('kind'))

            queryset = Note.objects.filter(vehicle__id=vehicle_id, kind__id=kind_id)
            serializer = self.get_serializer(queryset, many=True)
            return Response(serializer.data)

        except TypeError:
            return Response(
                {'message': 'Mandatory params missed: vehicle and/or kind.'},
                status=status.HTTP_400_BAD_REQUEST
            )

