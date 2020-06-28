import json

from django.db.models import Q
from rest_framework import serializers
from rest_framework.response import Response

from GameModel.models import MagzineScores, Shelf, Subjects, Currency
from link.util import OssManager

import json


class MagzineScoresSerializer(serializers.HyperlinkedModelSerializer):
    shelf = serializers.SerializerMethodField()

    class Meta:
        model = MagzineScores
        fields = ("id", "gameId", "magazine", "score", "scoreWord", "subject", "comment",
                  "comment_trans", "shelf", "url")
        # fields = ("__all__")

    def get_shelf(self, object):
        shelf = Shelf.objects.filter(gameId=object.gameId).first()

        if shelf is not None:
            return ShelfSerializer(instance=shelf).data
        else:
            return None


class SubjectsSerializer(serializers.HyperlinkedModelSerializer):
    latestPriceCNY = serializers.SerializerMethodField()

    def list(self, request, *args, **kwargs):
        print("over ride")
        if request.GET["officialGameId"]:
            one = Subjects.objects.filter(officialGameId=request.GET["officialGameId"]).first()

            serializer = self.get_serializer(one)
            return Response(serializer.data)
        else:
            super(SubjectsSerializer, self).list(self, request)

    class Meta:
        model = Subjects
        fields = ("__all__")

    def get_latestPriceCNY(self, obj):
        print(obj)
        # 货币转换
        (latestCNY, updated) = Currency.getLatestAmount(obj.currency, obj.latestPrice)
        return latestCNY


class ShelfSerializer(serializers.HyperlinkedModelSerializer):
    subjects = serializers.SerializerMethodField()
    intro = serializers.SerializerMethodField()
    mp_cover = serializers.SerializerMethodField()
    mp_cover_detail = serializers.SerializerMethodField()
    mp_thumb = serializers.SerializerMethodField()
    related = serializers.SerializerMethodField()

    class Meta:
        model = Shelf
        fields = ("gameId", "titleCh", "hasChinese", "keyword", "cover", "mp_cover",
                  "mp_cover_detail", "thumb", "mp_thumb", "subjects", "score", "intro",
                  "related")

    def get_subjects(self, obj):
        data = Subjects.objects.filter(officialGameId__in=obj.officialGameIds.split(','))

        list = []
        # 放入迭代器
        for item in data:
            list.append(SubjectsSerializer(item).data)
        return list

    def get_intro(self, obj):
        intro = json.loads(json.dumps(eval(obj.intro)))
        res = ""
        if "hk" in intro:
            res = intro["hk"]
        elif "trans" in intro:
            res = intro["trans"]
        # 去掉PSN游戏介绍里的copyright信息
        if res.find("<b>Copyright：</b>") > 0:
            res = res[0:res.find("<b>Copyright：</b>")]
        return res

    def get_mp_cover(self, obj):
        cover_str = obj.cover.replace("\'", "\"")
        cover_list = json.loads(cover_str, encoding="utf-8")
        res = []
        om = OssManager()
        for item in cover_list:
            if not item.startswith("http"):
                res.append(om.get_url(item, "cover", "mp_list_icon_w60h60"))
        return res

    def get_mp_cover_detail(self, obj):
        cover_str = obj.cover.replace("\'", "\"")
        cover_list = json.loads(cover_str, encoding="utf-8")
        res = []
        om = OssManager()
        for item in cover_list:
            if not item.startswith("http"):
                res.append(om.get_url(item, "cover", "mp_detail_pic_w414"))
        return res

    def get_mp_thumb(self, obj):
        thumb_str = obj.thumb.replace("\'", "\"")
        thumb_list = json.loads(thumb_str, encoding="utf-8")
        res = []
        om = OssManager()
        for item in thumb_list[:8]:
            if not item.startswith("http"):
                res.append(om.get_url(item, "thumb", "mp_detail_pic_w414h240"))
        return res

    # 相关游戏
    def get_related(self, obj):
        list = []
        if obj.serial_id != 0:
            related = Shelf.objects.filter(serial__id=obj.serial_id).filter(~Q(gameId=obj.gameId)).order_by("titleCh")
            for r in related:
                list.append(RelatedSerializer(r).data)
        return list


# 相关游戏单独建一个迭代器，否则related会导致数据无限循环
class RelatedSerializer(ShelfSerializer):
    class Meta:
        model = Shelf
        fields = ("gameId", "titleCh", "hasChinese", "cover", "mp_cover",
                  "mp_cover_detail", "score")
