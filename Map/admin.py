from django.contrib import admin
from . import  models
from .models import ImageModel
# Register your models here.

admin.site.register(models.GeoJSONData)


@admin.register(ImageModel)
class ImageModelAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at', 'updated_at')
    search_fields = ('name',)

