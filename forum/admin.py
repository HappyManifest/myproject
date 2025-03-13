from django.contrib import admin
from .models import Post, Comment

class PostAdmin(admin.ModelAdmin):
    # 定义显示的字段
    list_display = ('title', 'author', 'created_at', 'updated_at')
    # 定义可以在后台搜索的字段
    search_fields = ('title', 'content', 'author__username')  # 允许通过标题、内容和用户名搜索
    # 定义排序规则，按创建时间倒序
    ordering = ('-created_at',)
    # 定义可以过滤的字段（比如按作者过滤）
    list_filter = ('author', 'created_at')
    # 添加可编辑字段
    list_editable = ('title',)
    # 设置哪个字段可以点击查看详细信息
    list_display_links = ('author',)  # 你可以指定作者字段为可点击的链接

class CommentAdmin(admin.ModelAdmin):
    list_display = ('author', 'post', 'created_at', 'content', 'image')  # 显示的字段
    list_filter = ('post', 'author')  # 可以过滤的字段
    search_fields = ('content', 'author__username', 'post__title')  # 搜索字段
    list_per_page = 10  # 每页显示的条数
    ordering = ('-created_at',)  # 默认排序按创建时间降序

    # 显示评论时的头像和用户名（如果需要的话）
    def author_avatar(self, obj):
        # 确保引用的是小写的 "head" 字段
        if obj.author.head:
            return f'<img src="{obj.author.head.url}" style="width: 40px; height: 40px;" />'
        return 'No Avatar'
    author_avatar.allow_tags = True
    author_avatar.short_description = 'Avatar'

    # 让评论内容在列表页面显示更多信息
    def content_preview(self, obj):
        return obj.content[:50]  # 显示评论内容的前50个字符
    content_preview.short_description = 'Content Preview'

    # 不允许在表单中编辑 created_at 字段
    exclude = ('created_at',)  # 不允许在表单中编辑 created_at 字段

    # 设置表单字段（不包括 created_at）
    def get_fields(self, request, obj=None):
        if not obj:  # 新增时
            return ['author', 'post', 'content', 'image']
        return ['author', 'post', 'content', 'image']  # 修改时不显示 created_at 字段

admin.site.register(Post, PostAdmin)
admin.site.register(Comment, CommentAdmin)
