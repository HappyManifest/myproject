from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
app_name = 'index'
urlpatterns = [
      path('',views.index_view)]