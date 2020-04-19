from rest_framework import serializers
from rest_framework.settings import api_settings
from .models import Kind, Note
from .relations import KindRelatedField, VehicleRelatedField
from django.core.files.uploadedfile import TemporaryUploadedFile, InMemoryUploadedFile


class KindSerializer(serializers.ModelSerializer):
    class Meta:
        model = Kind
        fields = ('id', 'slug', 'title',)


class NoteListSerializer(serializers.ModelSerializer):
    created = serializers.DateField(format=api_settings.DATE_FORMAT, read_only=True)
    updated = serializers.DateField(format=api_settings.DATE_FORMAT, read_only=True)

    class Meta:
        model = Note
        fields = (
            'id', 'created', 'updated',
            'title', 'run', 'cost', 'attachment1',
        )


class NoteSerializer(serializers.ModelSerializer):
    vehicle = VehicleRelatedField(write_only=True)
    kind = KindRelatedField(write_only=True)

    created = serializers.DateField(format=api_settings.DATE_FORMAT, read_only=True)
    updated = serializers.DateField(format=api_settings.DATE_FORMAT, read_only=True)

    class Meta:
        model = Note
        fields = (
            'id', 'vehicle', 'kind', 'created', 'updated',
            'title', 'content', 'run', 'cost', 'attachment1', 'attachment2', 'attachment3',
        )

    def to_internal_value(self, data):
        # Catch empty optional fields value and set em to None.
        # Do it because of javascript FormData cannot send NULL to server lol.
        int_fields = ('run', 'cost',)
        file_fields = ('attachment1', 'attachment2', 'attachment3',)
        ret = {}

        for k in data:

            if k in int_fields:
                try:
                    v = int(data.get(k))
                except ValueError:
                    v = None

            elif k in file_fields:
                if type(data.get(k)) is TemporaryUploadedFile or type(data.get(k)) is InMemoryUploadedFile:
                    v = data.get(k)
                else:
                    v = None

            else:
                v = data.get(k)

            ret[k] = v

        return super(NoteSerializer, self).to_internal_value(ret)
