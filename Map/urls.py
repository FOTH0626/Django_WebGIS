from django.urls import path
from django.views.generic import TemplateView
from . import views

urlpatterns = [
    path("",TemplateView.as_view(template_name="map.html")),
    path("api/geojson/<int:pk>/",views.get_geojson_by_id),
    path("api/tiff/<int:pk>/",views.get_geotiff_by_id),
    path("api/image/coordinates/<int:image_id>/",views.get_image_coordinates),
    path("api/image/file/<int:image_id>/",views.get_image_file),
    path("api/diffmap/<int:image_id1>/<int:image_id2>/",views.light_change_diffmap),
    path("api/binary_diffmap/<int:image_id1>/<int:image_id2>/",views.light_change_diffmap_binary),
]