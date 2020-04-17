from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser
from django.db.models import Count
from rest_framework.exceptions import PermissionDenied

from ..vehicles.serializers import VehicleSerializer

User = get_user_model()


class UserRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'email', 'password',)
        context_required = True
        extra_kwargs = {
            'password': {'write_only': True},
            'email': {'required': True}
        }

    def create(self, validated_data):
        # TODO: Consider moving this code to View
        request = self.context.get('request')

        if type(request.user) is not AnonymousUser:
            raise PermissionDenied

        user = self.Meta.model(email=validated_data['email'])
        user.set_password(validated_data['password'])
        user.save()

        return user


class UserCurrentSerializer(serializers.ModelSerializer):
    vehicles = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('id', 'email', 'vehicles')

    def get_vehicles(self, user):
        vehicles = user.vehicles.annotate(notes_count=Count('notes'))
        serializer = VehicleSerializer(vehicles, many=True)
        return serializer.data

