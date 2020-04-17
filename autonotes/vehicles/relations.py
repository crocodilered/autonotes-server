from rest_framework import serializers
from .models import Model


class ModelRelatedField(serializers.RelatedField):
    def get_queryset(self):
        return Model.objects.all()

    def to_internal_value(self, data):
        model_id = int(data)
        return Model.objects.get(id=model_id)

    def to_representation(self, model):
        from .serializers import ModelSerializer
        serializer = ModelSerializer(model)
        return serializer.data

