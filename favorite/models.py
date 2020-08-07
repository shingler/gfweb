import time

from django.contrib.auth.models import User
from django.db import models

from django.db import models
from GameModel.models import Shelf


class Favorite(models.Model):
    id = models.AutoField(verbose_name="主键", primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="用户ID")
    shelf = models.ForeignKey(Shelf, on_delete=models.CASCADE, verbose_name="游戏库ID")
    state = models.BooleanField(default=True, verbose_name="收藏状态")
    created = models.IntegerField(verbose_name="创建时间", default=time.time())
    updated = models.IntegerField(verbose_name="更新时间", default=time.time(), db_index=True)

    class Meta:
        db_table = "favorite"
        unique_together = ["user", "shelf"]
