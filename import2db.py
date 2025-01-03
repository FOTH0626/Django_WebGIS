import json
from Map.models import GeoJSONData
from django.core.management.base import BaseCommand


def import_geojson(file_path):
    """
    从本地文件导入GeoJSON数据到数据库

    Args:
        /file_path (str): GeoJSON文件的路径
    """
    try:
        # 读取GeoJSON文件
        with open(file_path, 'r', encoding='utf-8') as file:
            geojson_data = json.load(file)

        # 提取需要的数据
        name = geojson_data.get('name', '')
        features = geojson_data.get('features', [])

        # 创建数据库记录
        geojson_obj = GeoJSONData(
            name=name,
            features=features
        )
        geojson_obj.save()

        return True, f"Successfully imported {name}"

    except FileNotFoundError:
        return False, "File not found"
    except json.JSONDecodeError:
        return False, "Invalid JSON format"
    except Exception as e:
        return False, f"Error occurred: {str(e)}"


# 如果你想要创建一个Django管理命令，可以这样做：
class Command(BaseCommand):
    help = 'Import GeoJSON data from local file'

    def add_arguments(self, parser):
        parser.add_argument('file_path', type=str, help='Path to the GeoJSON file')

    def handle(self, *args, **options):
        success, message = import_geojson(options['file_path'])
        if success:
            self.stdout.write(self.style.SUCCESS(message))
        else:
            self.stdout.write(self.style.ERROR(message))
