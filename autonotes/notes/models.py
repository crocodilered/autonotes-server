from django.db import models

from ..vehicles.models import Vehicle
from ..tags.models import Tag

from .paths import attachments_path


class Kind(models.Model):
    slug = models.CharField(max_length=50, unique=True)
    title = models.CharField(max_length=50)

    def __str__(self):
        return self.title


class Note(models.Model):
    kind = models.ForeignKey(
        Kind,
        related_name='notes',
        db_index=True,
        on_delete=models.CASCADE
    )

    vehicle = models.ForeignKey(
        Vehicle,
        related_name='notes',
        db_index=True,
        on_delete=models.CASCADE
    )

    tags = models.ManyToManyField(Tag, related_name='notes')

    title = models.CharField(max_length=200)
    content = models.TextField(null=True, blank=True)

    shared = models.BooleanField(default=False, db_index=True,)

    attachment1 = models.FileField(upload_to=attachments_path, null=True)
    attachment2 = models.FileField(upload_to=attachments_path, null=True)
    attachment3 = models.FileField(upload_to=attachments_path, null=True)

    cost = models.PositiveIntegerField(null=True, blank=True, default=None)
    run = models.PositiveIntegerField(null=True, blank=True, default=None)

    created = models.DateField(auto_now_add=True, db_index=True)
    updated = models.DateField(auto_now=True)

    class Meta:
        ordering = ('-created', '-id')

    def __str__(self):
        return self.title
