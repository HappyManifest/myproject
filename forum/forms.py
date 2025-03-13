from django import forms
from .models import Post, Comment

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content', 'image']
class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content', 'image']
class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content', 'image']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '请输入帖子标题'}),
            'content': forms.Textarea(attrs={'class': 'form-control', 'rows': 6, 'placeholder': '请输入帖子内容...'}),
        }