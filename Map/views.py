# Map/views.py
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from django.http import FileResponse
from django.http import HttpResponse
from PIL import Image
import numpy as np
import io


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



@api_view(['GET'])
def light_change_diffmap(request, image_id1, image_id2):
    # 获取数据库中的图像对象
    image1 = ImageModel.objects.get(id=image_id1)
    image2 = ImageModel.objects.get(id=image_id2)

    # 打开并转换图像为灰度图
    img1 = Image.open(image1.image.path).convert("L")
    img2 = Image.open(image2.image.path).convert("L")

    # 调整图像尺寸一致
    if img1.size != img2.size:
        img1 = img1.resize(img2.size)

    # 将图像转换为 NumPy 数组
    data1 = np.array(img1, dtype=np.int16)
    data2 = np.array(img2, dtype=np.int16)

    # 计算差异矩阵并裁剪范围
    diff = np.clip(data2 - data1, -255, 255)

    # 创建渐变热力图
    diffmap = np.zeros((diff.shape[0], diff.shape[1], 3), dtype=np.uint8)

    # 获取正负最大值
    max_positive = diff[diff > 0].max() if (diff > 0).any() else 1
    max_negative = diff[diff < 0].min() if (diff < 0).any() else -1

    # 使用对数函数增强对比度
    def enhance(value, max_value):
        return (np.log1p(value) / np.log1p(max_value) * 255).astype(np.uint8)

    # 红色渐变（正差值）
    positive_values = np.where(diff > 0, diff, 0)
    diffmap[..., 0] = enhance(positive_values, max_positive)

    # 绿色渐变（负差值）
    negative_values = np.where(diff < 0, -diff, 0)
    diffmap[..., 1] = enhance(negative_values, -max_negative)

    # 将 NumPy 数组转换为 PIL 图像
    diffmap_img = Image.fromarray(diffmap, mode="RGB")

    # 将图像保存到内存中
    buffer = io.BytesIO()
    diffmap_img.save(buffer, format="PNG")
    buffer.seek(0)

    # 返回图像作为 HTTP 响应
    return HttpResponse(buffer, content_type="image/png")

@api_view(['GET'])
def light_change_diffmap_binary(request, image_id1, image_id2):
    # 文件路径（替换为实际路径）
    image1 = ImageModel.objects.get(id=image_id1)
    image2 = ImageModel.objects.get(id=image_id2)

    img1 = Image.open(image1.image.path).convert("L")
    img2 = Image.open(image2.image.path).convert("L")

    if img1.size != img2.size:
       img1 = img1.resize(img2.size)

    # 将图像转换为 NumPy 数组
    data1 = np.array(img1, dtype=np.int16)
    data2 = np.array(img2, dtype=np.int16)

    # 计算差异矩阵
    diff = data2 - data1
    diff = np.clip(diff, -255, 255)

    # 创建 RGB 热力图
    diffmap = np.zeros((diff.shape[0], diff.shape[1], 3), dtype=np.uint8)

    # 红色表示增加（差异 > 0）
    diffmap[diff > 0] = [255, 0, 0]

    # 绿色表示减少（差异 < 0）
    diffmap[diff < 0] = [0, 255, 0]

    # 黑色表示无变化（差异 = 0），默认保持为 [0, 0, 0]

    # 将 NumPy 数组转换为 PIL 图像
    diffmap_img = Image.fromarray(diffmap, mode="RGB")

    # 将图像保存到内存中
    buffer = io.BytesIO()
    diffmap_img.save(buffer, format="PNG")
    buffer.seek(0)

    # 返回图像作为 HTTP 响应
    return HttpResponse(buffer, content_type="image/png")