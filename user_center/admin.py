from django.contrib import admin
from .models import User  # 导入 User 模型

class UserAdmin(admin.ModelAdmin):
    list_display = ('Username', 'Phone', 'Email', 'created_time', 'update_time')
    search_fields = ('Username', 'Phone', 'Email')
    list_filter = ('created_time', 'update_time')

admin.site.register(User, UserAdmin)

# Register your models here.
