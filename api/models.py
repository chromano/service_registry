from django.db import models


class Service(models.Model):
    name = models.CharField(max_length=255)
    version = models.CharField(max_length=12)
    url = models.URLField()

    class Meta:
        unique_together = ('name', 'version', 'url')
