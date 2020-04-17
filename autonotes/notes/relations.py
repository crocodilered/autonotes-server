from rest_framework import serializers
from autonotes.vehicles.models import Vehicle
from .models import Kind


class KindRelatedField(serializers.RelatedField):
    def get_queryset(self):
        return Kind.objects.all()

    def to_internal_value(self, pk):
        return Kind.objects.get(id=int(pk))

    def to_representation(self, kind):
        return kind.pk


class VehicleRelatedField(serializers.RelatedField):
    def get_queryset(self):
        return Vehicle.objects.all()

    def to_internal_value(self, pk):
        return Vehicle.objects.get(id=int(pk))

    def to_representation(self, vehicle):
        return vehicle.pk
