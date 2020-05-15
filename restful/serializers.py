import json

from rest_framework import serializers
from rest_framework.response import Response

from GameModel.models import MagzineScores, Shelf, Subjects, Currency


class MagzineScoresSerializer(serializers.HyperlinkedModelSerializer):
    shelf = serializers.SerializerMethodField()

    class Meta:
        model = MagzineScores
        fields = ("id", "gameId", "magazine", "score", "scoreWord", "subject", "comment", "comment_trans", "shelf", "url")
        # fields = ("__all__")

    def get_shelf(self, object):
        shelf = Shelf.objects.filter(gameId=object.gameId).first()
        if shelf is not None:
            # 取单图
            covers = json.loads(shelf.cover.replace("\'", "\""))
            if len(covers) > 0:
                shelf.cover = covers[0]
            thumbs = json.loads(shelf.thumb.replace("\'", "\""))
            if len(thumbs) > 0:
                shelf.thumb = thumbs[0]
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
        # 货币转换
        (latestCNY, updated) = Currency.getLatestAmount(obj.currency, obj.latestPrice)
        return latestCNY


class ShelfSerializer(serializers.HyperlinkedModelSerializer):
    subjects = serializers.SerializerMethodField()
    intro = serializers.SerializerMethodField()

    class Meta:
        model = Shelf
        fields = ("gameId", "titleCh", "hasChinese", "keyword", "cover", "thumb", "subjects", "score", "intro")

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
