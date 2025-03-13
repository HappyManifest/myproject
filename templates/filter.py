from django import template

register = template.Library()

@register.filter(name='nl2br')
def nl2br(value):
    """将换行符替换为 <br> 标签"""
    return value.replace('\n', '<br>\n')
