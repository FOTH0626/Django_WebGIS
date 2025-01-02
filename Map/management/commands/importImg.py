import os
from django.core.management.base import BaseCommand
from django.core.exceptions import ValidationError
from Map.models import SatelliteImage
from osgeo import gdal

class Command(BaseCommand):
    help = 'Import satellite image metadata from a local file into the database'

    def add_arguments(self, parser):
        parser.add_argument('file_path', type=str, help='Path to the satellite image file (RRD or IMG)')

    def handle(self, *args, **options):
        file_path = options['file_path']

        try:
            if not os.path.exists(file_path):
                raise FileNotFoundError(f"File not found: {file_path}")

            # Open the file using GDAL
            dataset = gdal.Open(file_path)
            if not dataset:
                raise ValidationError(f"Unable to open file with GDAL: {file_path}")

            # Extract metadata
            file_name = os.path.basename(file_path)
            file_size = os.path.getsize(file_path)
            num_bands = dataset.RasterCount
            geo_transform = dataset.GetGeoTransform()
            resolution_x = geo_transform[1] if geo_transform else None
            resolution_y = -geo_transform[5] if geo_transform else None

            # Determine file type
            file_extension = os.path.splitext(file_name)[1].lower()
            if file_extension == '.rrd':
                file_type = 'RRD'
            elif file_extension == '.img':
                file_type = 'IMG'
            else:
                raise ValidationError(f"Unsupported file type: {file_extension}")

            # Create a new SatelliteImage record
            satellite_image = SatelliteImage(
                name=file_name,
                rrd_file=file_path if file_type == 'RRD' else None,
                img_file=file_path if file_type == 'IMG' else None,
                file_size=file_size,
                num_bands=num_bands,
                resolution_x=resolution_x,
                resolution_y=resolution_y
            )
            satellite_image.clean()  # Validate model fields
            satellite_image.save()

            self.stdout.write(self.style.SUCCESS(f"Successfully imported {file_name} into the database"))

        except FileNotFoundError as e:
            self.stdout.write(self.style.ERROR(str(e)))
        except ValidationError as e:
            self.stdout.write(self.style.ERROR(f"Validation error: {e.message}"))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"An unexpected error occurred: {str(e)}"))
