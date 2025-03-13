from django.contrib.gis.db import models

class Province(models.Model):
    name = models.CharField(max_length=50, unique=True)
    geometry = models.PolygonField()
    air_quality_index = models.FloatField()
    water_quality_index = models.FloatField()
    noise_pollution = models.FloatField()
    industrial_emissions = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.name
class City(models.Model):
    name = models.CharField(max_length=50)
    province = models.ForeignKey(Province, on_delete=models.CASCADE, related_name="cities")
    geometry = models.PointField()
    air_quality_index = models.FloatField()
    water_quality_index = models.FloatField()
    noise_pollution = models.FloatField()
    industrial_emissions = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"{self.name}, {self.province.name}"
