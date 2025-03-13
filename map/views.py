from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import Province, City
import requests
import os
from django.contrib.gis.serializers import geojson

@api_view(['GET'])
def get_provinces(request):
    provinces = Province.objects.all()
    provinces_geojson = geojson.Serializer().serialize(provinces)
    return Response({'provinces': provinces_geojson})

@api_view(['GET'])
def get_cities(request, province_name):
    cities = City.objects.filter(province__name=province_name)
    cities_geojson = geojson.Serializer().serialize(cities)
    return Response({'cities': cities_geojson})
from django.core.cache import cache

@api_view(['GET'])
def get_environment_data(request, city_name):
    cache_key = f'weather_data_{city_name}'
    cached_data = cache.get(cache_key)

    if cached_data:
        return Response({'weather_data': cached_data})

    API_KEY = os.getenv('BAIDU_API_KEY')
    url = f"https://api.map.baidu.com/telematics/v3/weather?location={city_name}&output=json&ak={API_KEY}"

    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()

        if data['status'] == 'success':
            weather_info = data['results'][0]['weather_data'][0]
            weather_data = {
                'city': city_name,
                'temperature': weather_info.get('temperature'),
                'weather': weather_info.get('weather'),
                'wind': weather_info.get('wind'),
                'time': weather_info.get('date')
            }
            cache.set(cache_key, weather_data, timeout=3600)  # 缓存1小时
            return Response({'weather_data': weather_data})
        else:
            return Response({'error': 'Weather data not found'}, status=400)
    except requests.exceptions.RequestException as e:
        return Response({'error': str(e)}, status=500)