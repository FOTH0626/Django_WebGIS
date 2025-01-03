#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import rasterio
from rasterio.transform import Affine
from pyproj import Transformer
import sys

def geotiff_corners(geotiff_path):
    """
    输出 GeoTIFF 文件四个角的 WGS84 坐标。

    Args:
        geotiff_path (str): GeoTIFF 文件的路径。
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
            if crs == "EPSG:4326":
                corners_wgs84 = corners_geo
            elif crs is not None:
                transformer = Transformer.from_crs(crs, "EPSG:4326", always_xy=True)
                corners_wgs84 = [transformer.transform(x, y) for x, y in corners_geo]
            else:
                corners_wgs84 = [(None, None)] * 4
                print("警告：GeoTIFF 文件缺少 CRS 信息，无法转换为 WGS84 坐标")
            
            # 输出 WGS84 坐标
            print("四个角的 WGS84 坐标 (左上, 右上, 左下, 右下):")
            for i, (lon, lat) in enumerate(corners_wgs84):
                if lon is not None and lat is not None:
                    print(f"  角 {i+1}: 经度 = {lon:.9}, 纬度 = {lat:.9}")
                else:
                    print(f"  角 {i+1}: 坐标转换失败")
    except Exception as e:
        print(f"发生错误: {e}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print(f"用法: python {sys.argv[0]} <输入GeoTIFF路径>")
        sys.exit(1)

    geotiff_file = sys.argv[1]
    geotiff_corners(geotiff_file)