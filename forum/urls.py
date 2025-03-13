from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
app_name = 'forum'

urlpatterns = [
      path('',views.post_list),
      path('post/<int:post_id>/', views.post_detail, name='post_detail'),
      path('create/', views.create_post, name='create_post'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)