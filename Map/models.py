from django.db import models
from django.contrib.gis.db import models as geoModels
# Create your models here.

class GeoJSONData(models.Model):
    name = models.CharField(max_length=255)
    crs_type = models.CharField(max_length=255)
    crs_properties = models.JSONField()
    features = models.JSONField()

    def __str__(self):
        return self.name

class ShapeFileData(geoModels.Model):
    name = models.CharField(max_length=255)
    crs_type = models.CharField(max_length=255)
    crs_properties = models.JSONField()
    features = models.JSONField()

    def __str__(self):
        return self.name
