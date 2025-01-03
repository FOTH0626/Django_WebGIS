from django.db import models
from django.contrib.gis.db import models as geoModels
# Create your models here.

class GeoJSONData(models.Model):
    name = models.CharField(max_length=255)
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


class GeoTIFFData(models.Model):
    name = models.CharField(max_length=255)
    data = models.FileField()

    def __str__(self):
        return self.name


from django.db import models


class ImageModel(models.Model):
    # 图片名称
    name = models.CharField(max_length=255, verbose_name="Image Name")

    # 上传的图片文件，限制为 PNG 格式
    image = models.ImageField(
        upload_to='images/',
        verbose_name="Image File",
        help_text="Only PNG files are allowed."
    )

    # 左下角经纬度
    southwest_lat = models.DecimalField(
        max_digits=9,
        decimal_places=6,
        verbose_name="Southwest Latitude"
    )
    southwest_lng = models.DecimalField(
        max_digits=9,
        decimal_places=6,
        verbose_name="Southwest Longitude"
    )

    # 右上角经纬度
    northeast_lat = models.DecimalField(
        max_digits=9,
        decimal_places=6,
        verbose_name="Northeast Latitude"
    )
    northeast_lng = models.DecimalField(
        max_digits=9,
        decimal_places=6,
        verbose_name="Northeast Longitude"
    )

    # 时间戳
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Created At")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Updated At")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Image Model"
        verbose_name_plural = "Image Models"
