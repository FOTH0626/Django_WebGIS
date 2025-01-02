import os
from osgeo import gdal
from django.core.files import File
from django.core.management.base import BaseCommand
from Map.models import GeoTIFFData

class Command(BaseCommand):
    help = 'Import GeoTIFF data from a local file into the database'

    def add_arguments(self, parser):
        parser.add_argument('file_path', type=str, help='Path to the local GeoTIFF file')

    def handle(self, *args, **options):
        file_path = options['file_path']

        try:
            # Check if the file exists
            if not os.path.exists(file_path):
                self.stdout.write(self.style.ERROR("TIFF file not found"))
                return

            # Validate if the file is a valid GeoTIFF and has geographic information
            dataset = gdal.Open(file_path)
            if not dataset:
                self.stdout.write(self.style.ERROR("Invalid TIFF file or unable to open"))
                return

            geotransform = dataset.GetGeoTransform()
            if not geotransform or geotransform == (0, 1, 0, 0, 0, 1):
                self.stdout.write(self.style.ERROR("TIFF file lacks geographic information"))
                return

            tiff_name = os.path.basename(file_path)

            # Save to database using Django's File object
            with open(file_path, 'rb') as file:
                django_file = File(file)
                geo_tiff = GeoTIFFData(
                    name=tiff_name,
                    tiff=django_file
                )
                geo_tiff.save()

            self.stdout.write(self.style.SUCCESS(f"Successfully imported {tiff_name} into the database with geographic information"))

        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Error occurred: {str(e)}"))
