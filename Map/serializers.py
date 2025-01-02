# Map/serializers.py
from rest_framework import serializers
from .models import GeoJSONData

class GeoJSONDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = GeoJSONData
        fields = ['id', 'name', 'features']
