#生产地点: 杨浦公社技术部门
#生产时间: 2025/1/26 14:55
#生产者: 公社人民
#公社万岁
from django.urls import path,re_path
from . import views
app_name = 'user_center'
urlpatterns=[
    path('register',views.register_final),
    path('login',views.login_view,name='login'),
    path('logout',views.logout_view,name='logout'),
    path('email1',views.register_view),
    path('personal_zone',views.personal_zone),
    re_path(r'^verify_code$',views.verify_code),
    re_path(r'^url_reverse$', views.url_reverse),
    path('send_emaill',views.send),
    path('edit_profile',views.edit_profile),
    path('change_password2',views.change_password2),
    path('change_password',views.change_password,name='change_password'),
    path('<str:username>/', views.personal_zone2, name='personal_zone2'),
]

