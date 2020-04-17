from django.db import models


class TitledModel(models.Model):
    slug = models.CharField(max_length=50, unique=True)
    title = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.title

    class Meta:
        abstract = True
        ordering = ('title',)
