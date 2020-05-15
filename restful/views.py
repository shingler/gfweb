import json

from rest_framework import request

from GameModel.models import MagzineScores, Subjects, Shelf, Currency
from restful.serializers import MagzineScoresSerializer, SubjectsSerializer, ShelfSerializer
from rest_framework import viewsets, generics, renderers
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse


@api_view(['GET'])
def api_root(request, format=None):
    return Response({
        'games': reverse('shelf-list', request=request, format=format),
        'magzine': reverse('magzine-list', request=request, format=format),
        'subject': reverse('subject-list', request=request, format=format)
    })


class GameHighLight(generics.GenericAPIView):
    queryset = Shelf.objects.all()
    renderer_classes = (renderers.StaticHTMLRenderer,)

    def get(self, request, *args, **kwargs):
        snippet = self.get_object()
        return Response(snippet.highlighted)


class SubjectsViewSet(viewsets.ModelViewSet):
    queryset = Subjects.objects.all().order_by("-officialGameId")
    serializer_class = SubjectsSerializer
    lookup_field = "officialGameId"

    def retrieve(self, request, *args, **kwargs):
        ogi = kwargs.get("officialGameId")
        print(kwargs)
        if ogi:
            sub = Subjects.objects.filter(officialGameId=ogi).first()
            return Response(SubjectsSerializer(instance=sub).data)
        else:
            return Response("not found")


class ShelfViewSet(viewsets.ModelViewSet):
    queryset = Shelf.objects.all().order_by("-gameId")
    serializer_class = ShelfSerializer

    def retrieve(self, request, *args, **kwargs):
        object = super(ShelfViewSet, self).get_object()
        if "one_cover" in request.GET and request.GET["one_cover"] == "1":
            covers = json.loads(object.cover.replace("\'", "\""))
            object.cover = covers[0]
        return Response(ShelfSerializer(instance=object).data)

    def list(self, request, *args, **kwargs):
        if "keyword" in request.GET and len(request.GET["keyword"]) > 0:
            self.queryset = Shelf.objects.filter(keyword__icontains=request.GET["keyword"]).order_by("-gameId")
        return super(ShelfViewSet, self).list(request, args, kwargs)


class MagzineViewSet(viewsets.ModelViewSet):
    queryset = MagzineScores.objects.all().order_by("-gameId")
    serializer_class = MagzineScoresSerializer
    # lookup_url_kwarg = "gameId"

    def list(self, request, *args, **kwargs):
        # print(kwargs, request.GET)
        gi = request.GET["gameId"]
        if gi:
            queryset = MagzineScores.objects.filter(gameId=gi)

        mags = []
        for item in queryset:
            mags.append(MagzineScoresSerializer(item).data)
        return Response(mags)


