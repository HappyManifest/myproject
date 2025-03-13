from django.urls import path
from . import views

app_name = 'volunteers'

urlpatterns = [
    path('', views.volunteer_activity_list, name='activity_list'),  # 活动列表页面
    path('create/', views.create_volunteer_activity, name='create_activity'),
    path('activity/<int:activity_id>/', views.volunteer_activity_detail, name='activity_detail'),
    path('edit/<int:activity_id>/', views.edit_activity, name='edit_activity'),
    path('delete/<int:activity_id>/', views.delete_activity, name='delete_activity'),
]
