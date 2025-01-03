from rasterio.transform import Affine
from pyproj import Proj, Transformer
from PIL import Image
import numpy as np
import rasterio
import sys

def geotiff_to_png_with_corners(geotiff_path, png_path):
    """
    将单波段 GeoTIFF 文件转换为 PNG，并输出四个角的 WGS84 坐标。

    Args:
        geotiff_path (str): GeoTIFF 文件的路径。
        png_path (str): 输出 PNG 文件的路径。
    """
    try:
        with rasterio.open(geotiff_path) as src:
            # 获取仿射变换
            transform = src.transform
            # 获取图像的宽度和高度
            width = src.width
            height = src.height
            # 获取 GeoTIFF 的 CRS
            crs = src.crs

            # 定义四个角的像素坐标
            corners_pixel = [(0, 0), (width, 0), (0, height), (width, height)]

            # 将像素坐标转换为地理坐标
            corners_geo = [transform * corner for corner in corners_pixel]

            # 将 GeoTIFF 的 CRS 转换为 WGS84 (EPSG:4326)
            if crs is not None:
                transformer = Transformer.from_crs(crs, "EPSG:4326", always_xy=True)
                corners_wgs84 = [transformer.transform(x, y) for x, y in corners_geo]
            else:
                corners_wgs84 = [(None, None)] * 4
                print("警告：GeoTIFF 文件缺少 CRS 信息，无法转换为 WGS84 坐标")
            
            # 读取栅格数据
            raster_data = src.read(1)

            # 归一化栅格数据到 0-255，并转换为 8 位无符号整型
            if np.issubdtype(raster_data.dtype, np.floating):
                min_val = np.nanmin(raster_data)
                max_val = np.nanmax(raster_data)
                if max_val > min_val:
                    raster_data = ((raster_data - min_val) / (max_val - min_val) * 255).astype(np.uint8)
                else:
                    raster_data = np.zeros_like(raster_data, dtype=np.uint8)
            elif np.issubdtype(raster_data.dtype, np.integer):
                # 确保栅格数据是uint8
                if np.max(raster_data) > 255 or np.min(raster_data) < 0:
                   raster_data = np.clip(raster_data, 0, 255).astype(np.uint8)
                else:
                    raster_data = raster_data.astype(np.uint8)
            else:
                print(f"不支持的数据类型 {raster_data.dtype},请检查你的 GeoTiff 文件")
                return

            # 创建 PIL 图像
            image = Image.fromarray(raster_data)

            # 保存为 PNG
            image.save(png_path)

            # 输出 WGS84 坐标
            print("四个角的 WGS84 坐标 (左上, 右上, 左下, 右下):")
            for i, (lon, lat) in enumerate(corners_wgs84):
                if lon is not None and lat is not None:
                    print(f"  角 {i+1}: 经度 = {lon:.6f}, 纬度 = {lat:.6f}")
                else:
                    print(f"  角 {i+1}: 坐标转换失败")
    except Exception as e:
        print(f"发生错误: {e}")

if __name__ == "__main__":
    if len(sys.argv) == 2:
        print("输出 PNG 文件路径未指定，将使用输入 GeoTIFF 文件的路径")
        geotiff_file = sys.argv[1]
        png_file = f"{geotiff_file}.png"
    elif len(sys.argv) == 3:
        geotiff_file = sys.argv[1]
        png_file = sys.argv[2]
    else:
        print(f"用法: python {sys.argv[0]} <输入GeoTIFF路径> [输出PNG路径]")
        sys.exit(1)
    geotiff_to_png_with_corners(geotiff_file, png_file)
