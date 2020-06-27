import json

from django.db import models
import time


# 游戏系列表，用于游戏分类和相关推荐
class Serial(models.Model):
    id = models.AutoField(primary_key=True, verbose_name="主键")
    title = models.CharField(max_length=200, verbose_name="系列名称")
    # shelf = models.ForeignKey(Shelf, to_field="gameId", on_delete=models.SET_DEFAULT, default="")

    class Meta:
        db_table = "serial"


class Shelf(models.Model):
    # 游戏ID
    gameId = models.AutoField(primary_key=True, verbose_name="游戏ID")
    # 官方游戏ID
    officialGameIds = models.TextField(default="", verbose_name="官方游戏ID")
    # 中文名
    titleCh = models.CharField(max_length=100, default="", verbose_name="中文名")
    # 英文名
    titleEn = models.CharField(max_length=100, default="", verbose_name="英文名")
    # 日文名
    titleJp = models.CharField(max_length=100, default="", verbose_name="日文名")
    # 介绍
    intro = models.TextField(default="", verbose_name="介绍")
    # 封图汇总
    cover = models.TextField(default="", verbose_name="封图汇总")
    # 截图汇总
    thumb = models.TextField(default="", verbose_name="截图汇总")
    # 视频汇总
    video = models.TextField(default="", verbose_name="视频汇总")
    # 评分
    score = models.FloatField(default=0.0, verbose_name="评分")
    # 语言
    language = models.CharField(max_length=100, default="", verbose_name="语言")
    # 有无中文
    hasChinese = models.BooleanField(default=False, verbose_name="有无中文")
    # 系列ID
    serial = models.ForeignKey(to=Serial, default=0, verbose_name="系列ID", on_delete=models.SET_DEFAULT)
    # 关键词
    keyword = models.CharField(max_length=100, default="", verbose_name="关键词")
    # 游玩人数
    players = models.CharField(max_length=8, default="", verbose_name="游玩人数")
    # 游戏平台
    platform = models.CharField(max_length=50, default="", verbose_name="游戏平台")
    # 是否有联机
    online = models.BooleanField(default=False, verbose_name="是否有联机")
    # 游戏分级
    rate = models.CharField(max_length=200, default="", verbose_name="游戏分级")
    # 是否显示（用于隐藏重复或非中文版本）
    show = models.BooleanField(default=True, verbose_name="是否显示")

    @staticmethod
    def getData(gameId):
        data = Shelf.objects.get(gameId=gameId)
        games = Subjects.objects.filter(officialGameId__in=data.officialGameIds.split(","))
        data.__setattr__("games", games)
        data.cover = json.loads(json.dumps(eval(data.cover)))
        data.thumb = json.loads(json.dumps(eval(data.thumb)))
        return data

    class Meta:
        db_table = 'shelf'


class Subjects(models.Model):
    # 主键
    id = models.AutoField(primary_key=True, verbose_name="主键")
    # 官方游戏ID
    officialGameId = models.CharField(max_length=50, default="", verbose_name="官方游戏ID")
    # 游戏标题
    subject = models.CharField(max_length=100, default="", verbose_name="游戏标题")
    # 游戏介绍
    intro = models.TextField(verbose_name="游戏介绍")
    # 游戏封图
    cover = models.TextField(verbose_name="游戏封图")
    # 截图汇总
    thumb = models.TextField(verbose_name="截图汇总")
    # 视频汇总
    video = models.TextField(verbose_name="视频汇总")
    # 语言版本
    edition = models.CharField(max_length=100, default="", verbose_name="语言版本")
    # 发布日期
    publishDate = models.IntegerField(default=0, verbose_name="发布日期")
    # 发布日期字符串
    publishDateStr = models.CharField(max_length=20, default="", verbose_name="发布日期字符串")
    # 游玩人数
    players = models.CharField(max_length=20, default="", verbose_name="游玩人数")
    # 游戏分级
    rate = models.CharField(max_length=200, default="", verbose_name="游戏分级")
    # 货币名
    currency = models.CharField(max_length=20, default="", verbose_name="货币名")
    # 原价
    price = models.FloatField(default=0.0, verbose_name="原价")
    # 平台
    platform = models.CharField(max_length=100, default="", verbose_name="原价")
    # 销售区域
    saleArea = models.CharField(max_length=20, default="", verbose_name="销售区域")
    # 跳转地址
    url = models.CharField(max_length=200, default="", verbose_name="跳转地址")
    # 当前价
    latestPrice = models.FloatField(default=0.0, verbose_name="当前价")
    # 会员价格
    plusPrice = models.FloatField(default=0.0, verbose_name="会员价格")
    # 当前价截止日期
    latestExpire = models.IntegerField(default=0, verbose_name="当前价截止日期")
    # 会员价截止日期
    plusExpire = models.IntegerField(default=0, verbose_name="会员价截止日期")
    # 历史最低价
    historyPrice = models.FloatField(default=0.0, verbose_name="历史最低价")
    # 历史最低价日期
    hisDate = models.CharField(max_length=50, default="", verbose_name="历史最低价日期")
    # 创建日期
    created = models.IntegerField(default=0, verbose_name="创建日期")
    # 更新日期
    updated = models.IntegerField(default=0, verbose_name="更新日期")
    # 是否已关联游戏架
    onShelf = models.BooleanField(default=False, verbose_name="是否已关联游戏架")

    class Meta:
        db_table = 'subjects'


class MagzineScores(models.Model):
    MAG_CHOICE = ["gamespot", "metacritic", "Famitsu"]
    # 主键
    id = models.AutoField(primary_key=True, verbose_name="主键")
    # 游戏ID
    gameId = models.IntegerField(default=0, verbose_name="游戏ID")
    # 媒体名
    magazine = models.CharField(max_length=100, default="", verbose_name="媒体名")
    # 评分
    score = models.FloatField(default=0.0, verbose_name="评分")
    # 评分词
    scoreWord = models.CharField(max_length=20, default="", verbose_name="评分词")
    # 评分文章标题
    subject = models.CharField(max_length=200, default="", verbose_name="评分文章标题")
    # 评价
    comment = models.TextField(default="", verbose_name="评价")
    # 媒体评分稿url
    url = models.CharField(max_length=200, default="", verbose_name="媒体评分稿url")
    # 创建时间
    created = models.IntegerField(default=0, verbose_name="创建时间")
    # 被翻译的评价
    comment_trans = models.TextField(default="", verbose_name="被翻译的评价")

    # shelf = models.OneToOneField(Shelf, to_field="gameId", on_delete=models.CASCADE)

    class Meta:
        db_table = 'magzine_scores'

    @staticmethod
    def getMagzineNames():
        return MagzineScores.MAG_CHOICE


class Currency(models.Model):
    # 支持的货币种类
    supported_currency = ["HKD", "JPY", "USD", "ZAR"]
    # 源货币名
    currency = models.CharField(max_length=5, verbose_name="源货币名")
    # 转换成人民币的汇率
    rate = models.FloatField(default=0.0, verbose_name="转换成人民币的汇率")
    # 更新时间
    updated = models.IntegerField(default=0, verbose_name="更新时间")

    class Meta:
        db_table = 'currency'

    # 获得最新货币转换
    @staticmethod
    def getLatestAmount(cur, amount):
        if cur not in Currency.supported_currency:
            return False
        data = Currency.objects.filter(currency=cur).first()
        return amount * data.rate, data.updated


# 评分媒体，用于分类和爬虫设置
class Magazines(models.Model):
    id = models.AutoField(primary_key=True, verbose_name="主键")
    title = models.CharField(max_length=100, verbose_name="媒体名")
    domain = models.CharField(max_length=100, verbose_name="网站域名")
    list_url_template = models.CharField(max_length=200, verbose_name="列表页地址模板")
    platform = models.CharField(max_length=100, verbose_name="抓取的游戏平台")
    enable = models.BooleanField(default=True, verbose_name="是否启用")
    created = models.IntegerField(verbose_name="创建时间", default=int(time.time()))

    class Meta:
        db_table = "magazines"


# 游戏平台区域，用于分类和爬虫设置
class Platforms(models.Model):
    id = models.IntegerField(primary_key=True, verbose_name="主键")
    platform = models.CharField(max_length=100, default="", verbose_name="平台名")
    countryArea = models.CharField(max_length=20, default="", verbose_name="国家区域", null=False)
    countryAreaName = models.CharField(max_length=20, default="", verbose_name="国家区域名称", null=False)
    url = models.TextField(default="", verbose_name="爬虫地址模板", null=False)
    created = models.IntegerField(verbose_name="创建时间", default=int(time.time()))

    class Meta:
        db_table = "platforms"

    # @staticmethod

