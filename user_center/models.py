from django.db import models
from django.contrib.auth.models import AbstractUser

class User(models.Model):
    Username=models.CharField('用户名',max_length=30,unique=True)
    Password=models.CharField('密码',max_length=100)
    Phone=models.CharField('手机号',unique=True,   max_length=11)
    Email = models.EmailField('邮箱',default='1',blank=True,unique=True)
    Head=models.ImageField(upload_to='images',default='/media/images/山湖.jpg', blank=True,null=True)
    created_time=models.DateTimeField('创建时间',auto_now_add=True)
    update_time=models.DateTimeField('更新时间',auto_now=True)
    def __str__(self):
        return '%s'%(self.Username)
