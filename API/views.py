# Map/views.py
from rest_framework.response import Response
from rest_framework.decorators import api_view
from Map.models import GeoJSONData
from Map.serializers import GeoJSONDataSerializer
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


from Map.models import GeoTIFFData

@api_view(['GET'])
def get_tiff_by_id(request, pk):
    """
    根据ID查找TIFF文件并返回。
    """
    try:
        # 查找对应的 TIFF 数据
        tiff_data = GeoTIFFData.objects.get(id=pk)

        # 确保文件存在
        if not tiff_data.tiff:
            return Response({"error": "TIFF file not found"}, status=status.HTTP_404_NOT_FOUND)

        # 返回文件响应
        response = FileResponse(tiff_data.tiff.open('rb'), content_type='image/tiff')
        response['Content-Disposition'] = f'attachment; filename="{tiff_data.name}"'
        return response
    except GeoTIFFData.DoesNotExist:
        return Response({"error": "GeoTIFF data not found"}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
