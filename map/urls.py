#生产地点: 杨浦公社技术部门
#生产时间: 2025/1/26 14:53
#生产者: 公社人民
#公社万岁
from django.urls import path
from . import views

urlpatterns = [
    path('provinces/', views.get_provinces, name='get_provinces'),
    path('cities/<str:province_name>/', views.get_cities, name='get_cities'),
    path('environment/<str:city_name>/', views.get_environment_data, name='get_environment_data'),
]