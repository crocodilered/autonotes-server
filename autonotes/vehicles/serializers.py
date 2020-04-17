from rest_framework import serializers
from rest_framework.exceptions import PermissionDenied
from .relations import ModelRelatedField
from .models import Maker, Model, Vehicle


class MakerShortSerializer(serializers.ModelSerializer):
    class Meta:
        model = Maker
        fields = ('id', 'title',)


class ModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Model
        fields = ('id', 'title',)


class MakerRetrieveSerializer(serializers.ModelSerializer):
    models = ModelSerializer(many=True)

    class Meta:
        model = Maker
        fields = ('id', 'title', 'models',)


class VehicleSerializer(serializers.ModelSerializer):
    notes_count = serializers.IntegerField(required=False, read_only=True)
    maker = MakerShortSerializer(source='model.maker', required=False, read_only=True)
    model = ModelRelatedField()

    class Meta:
        model = Vehicle
        requires_context = True
        fields = ('id', 'maker', 'model', 'year', 'photo', 'notes_count',)

    def create(self, validated_data):
        request = self.context.get('request')

        if request.user.is_anonymous:
            raise PermissionDenied

        vehicle = self.Meta.model(
            user=request.user,
            model=validated_data['model'],
            year=validated_data.get('year'),
            photo=validated_data.get('photo')
        )

        vehicle.save()

        return vehicle

    def update(self, vehicle, validated_data):
        vehicle.year = validated_data.get('year', vehicle.year)
        vehicle.photo = validated_data.get('photo', vehicle.photo)
        vehicle.save()
        return vehicle
