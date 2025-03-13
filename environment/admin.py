from django.contrib import admin
from .models import Article
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'short_description', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('title', 'short_description')
    ordering = ('-created_at',)
from django.utils.html import mark_safe
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'short_description', 'created_at', 'image_preview')
    def image_preview(self, obj):
        if obj.image:
            return mark_safe('<img src="{0}" width="50" height="50" />'.format(obj.image.url))
        return "无图片"
    image_preview.short_description = '图片预览'

admin.site.register(Article, ArticleAdmin)

