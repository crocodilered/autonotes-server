from django.db import models

from ..core.models import TitledModel
from ..users.models import User

from .paths import vehicle_photos_path


class Maker(TitledModel):
    pass


class Model(models.Model):
    maker = models.ForeignKey(Maker, related_name='models', on_delete=models.CASCADE, db_index=True)

    slug = models.CharField(max_length=50)
    title = models.CharField(max_length=50)

    year_from = models.PositiveSmallIntegerField(null=True)
    year_to = models.PositiveSmallIntegerField(null=True)

    class Meta:
        unique_together = ('maker', 'title',)


class Vehicle(models.Model):
    model = models.ForeignKey(Model, on_delete=models.CASCADE, db_index=True)
    user = models.ForeignKey(User, related_name='vehicles', on_delete=models.CASCADE, db_index=True)

    photo = models.ImageField(upload_to=vehicle_photos_path, null=True)
    year = models.PositiveSmallIntegerField(null=True)

    created = models.DateField(auto_now_add=True)
    updated = models.DateField(auto_now=True)

    class Meta:
        ordering = ('id',)
