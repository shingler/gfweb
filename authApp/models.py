import time

from django.contrib.auth.models import User
from django.db import models

# Create your models here.


# 用户信息（扩展auth_user）
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name="外键user_id")
    avatar = models.CharField(max_length=256, verbose_name="头像地址")
    nickname = models.CharField(max_length=30, verbose_name="昵称")
    created = models.IntegerField(verbose_name="初次登录的时间", default=time.time())

    class Meta:
        db_table = "user_profile"


# 第三方登录信息
class Connect(models.Model):
    platform = (("wx", "微信"), ("alipay", "支付宝"))
    id = models.AutoField(primary_key=True, verbose_name="自增主键")
    user = models.ForeignKey(UserProfile, to_field="user_id", on_delete=models.SET_NULL, null=True, blank=True,
                             verbose_name="用户id")
    oauth_platform = models.CharField(max_length=10, choices=platform, verbose_name="第三方平台")
    oauth_platform_user_id = models.CharField(max_length=100, verbose_name="第三方平台唯一ID")
    oauth_key = models.CharField(max_length=128, verbose_name="第三方key")
    oauth_token = models.CharField(max_length=512, verbose_name="第三方token")
    oauth_token_fresh = models.CharField(max_length=512, verbose_name="第三方refresh token")
    oauth_expire = models.IntegerField(verbose_name="token有效期")
    oauth_token_fresh_expire = models.IntegerField(verbose_name="refresh token的有效期")
    oauth_data = models.TextField(verbose_name="oauth返回的数据")
    created = models.IntegerField(verbose_name="初次登录的时间", default=time.time())

    class Meta:
        db_table = "connect"
        index_together = ["oauth_platform", "oauth_platform_user_id"]


