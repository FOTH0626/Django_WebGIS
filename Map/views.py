# Map/views.py
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from django.http import FileResponse

from .models import GeoJSONData
from .serializers import GeoJSONDataSerializer
from .models import GeoTIFFData
from .models import ImageModel

@api_view(['GET'])
def get_geojson_by_id(request, pk):
    """
    根据ID查找GeoJSON数据并返回。
    """
    try:
        # 查找对应的 GeoJSON 数据
        geojson_data = GeoJSONData.objects.get(id=pk)
        # 使用序列化器将数据转为 JSON
        serializer = GeoJSONDataSerializer(geojson_data)
        return Response(serializer.data)
    except GeoJSONData.DoesNotExist:
        return Response({"error": "GeoJSON data not found"}, status=status.HTTP_404_NOT_FOUND)

@api_view(['GET'])
def get_geotiff_by_id(request, pk):
    """
    根据ID查找 GeoTIFF 数据并返回文件内容。
    """
    try:
        # 查找对应的 GeoTIFF 数据
        geotiff_data = GeoTIFFData.objects.get(id=pk)
        # 返回文件内容
        file_path = geotiff_data.data.path  # 获取文件的绝对路径
        return FileResponse(open(file_path, 'rb'), content_type='application/octet-stream')
    except GeoTIFFData.DoesNotExist:
        return Response({"error": "GeoTIFF data not found"}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
def get_image_coordinates(request, image_id):
    try:
        image = ImageModel.objects.get(id=image_id)
        data = {
            "southwest": {"lat": float(image.southwest_lat), "lng": float(image.southwest_lng)},
            "northeast": {"lat": float(image.northeast_lat), "lng": float(image.northeast_lng)},
        }
        return Response(data)
    except ImageModel.DoesNotExist:
        return Response({"error": "Image not found"}, status=404)

@api_view(['GET'])
def get_image_file(request, image_id):
    try:
        image = ImageModel.objects.get(id=image_id)
        return FileResponse(image.image.open(), content_type="image/png")
    except ImageModel.DoesNotExist:
        return Response({"error": "Image not found"}, status=404)
