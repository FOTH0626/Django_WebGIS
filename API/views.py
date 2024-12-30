# Map/views.py
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import GeoJSONData
from .serializers import GeoJSONDataSerializer
from rest_framework import status

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
