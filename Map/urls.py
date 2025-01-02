from django.urls import path
from django.views.generic import TemplateView
from . import views

urlpatterns = [
    path("",TemplateView.as_view(template_name="map.html")),
    path("api/geojson/<int:pk>/",views.get_geojson_by_id),
    path("api/tiff/<int:pk>/",views.get_geotiff_by_id),
]