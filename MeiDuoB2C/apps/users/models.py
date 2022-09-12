from django.db import models
# from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser

"""
自定义用户
"""
# class User(models.Model):
#     username = models.CharField(max_length=20, unique=True)
#     password = models.CharField(max_length=20)
#     mobile = models.CharField(max_length=11, unique=True)

"""
系统用户类(自定义)
我们的用户组和用户权限只能关联在一个用户表内
我们自己定义了一个用户表,系统还有一个用户表,因此就起了冲突
"""


class User(AbstractUser):
    mobile = models.CharField(max_length=11, unique=True)

    class Meta:
        verbose_name = '用户管理'
        verbose_name_plural = verbose_name
        db_table = 'tb_user'
