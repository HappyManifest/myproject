from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path('articles', views.article_list, name='article_list'),
    path('articles/<int:article_id>/', views.article_detail, name='article_detail'),
    path('search/', views.search, name='search'),
    path('crawl_articles/', views.crawl_articles_view, name='crawl_articles'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
