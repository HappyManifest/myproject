from rest_framework import serializers
from .models import Province, City

class ProvinceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Province
        fields = ['id', 'name', 'geometry']

class CitySerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = ['id', 'name', 'province', 'geometry', 'air_quality_index', 'water_quality_index', 'noise_pollution', 'industrial_emissions']