import json
from django.core.management.base import BaseCommand
from Map.models import GeoJSONData


class Command(BaseCommand):
    help = 'Import GeoJSON data from a local file into the database'

    def add_arguments(self, parser):
        parser.add_argument('file_path', type=str, help='Path to the local GeoJSON file')

    def handle(self, *args, **options):
        file_path = options['file_path']

        try:
            # 打开和读取GeoJSON文件
            with open(file_path, 'r', encoding='utf-8') as file:
                geojson_data = json.load(file)

            # 提取需要的数据
            name = geojson_data.get('name', '')
            crs = geojson_data.get('crs', {})
            crs_type = crs.get('type', '')
            crs_properties = crs.get('properties', {})
            features = geojson_data.get('features', [])

            # 创建一个新的数据库记录
            geojson_obj = GeoJSONData(
                name=name,
                crs_type=crs_type,
                crs_properties=crs_properties,
                features=features
            )
            geojson_obj.save()

            self.stdout.write(self.style.SUCCESS(f"Successfully imported {name} into the database"))

        except FileNotFoundError:
            self.stdout.write(self.style.ERROR("GeoJSON file not found"))
        except json.JSONDecodeError:
            self.stdout.write(self.style.ERROR("Invalid GeoJSON format"))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Error occurred: {str(e)}"))
