#!/usr/bin/python
# -*- coding:utf-8 -*-
# 评分/评论页面
import json
import math

import pysnooper
from django.http.response import HttpResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render
from GameModel.models import MagzineScores, Shelf
from .util import *

active = "comment"
theme = "weui"

# 媒体评分
# @pysnooper.snoop(watch_explode="paginator")
def magazine(request):
    # request数据
    get_data = request.GET.copy()
    page = get_data.setdefault("page", 1)
    # 根据媒体名查找评分
    magzine_name = get_data.setdefault("m", "")
    # 根据游戏名查找评分 @TODO
    game_name = get_data.setdefault("g", "")
    # 根据得分范围查找评分 @TODO
    score_low = get_data.setdefault("low", 1)
    score_high = get_data.setdefault("high", 10)
    # 页面样式
    theme = "bootstrap"
    if "theme" in request.GET and request.GET["theme"] in themes:
        theme = request.GET["theme"]

    # 获取数据
    size = 20
    total = MagzineScores.objects.count()
    page_count = math.ceil(total / size)
    filters = {}
    if len(magzine_name):
        filters["magazine"] = magzine_name
    if len(game_name):
        #@TODO 根据游戏名查找ID
        pass
    if score_low > 0:
        # filter["score"]
        pass

    mag_obj = MagzineScores()
    # magzines = MagzineScores.objects.filter(**filters)[offset:size]
    data_list = MagzineScores.objects.filter(**filters)
    # 分页
    paginator = Paginator(data_list, size)
    try:
        current_page_data = paginator.page(page)
    except PageNotAnInteger:
        current_page_data = paginator.page(1)
    except EmptyPage:
        current_page_data = paginator.page(paginator.num_pages)

    if theme == "weui":
        template = "weui/review/magazine.html"
    else:
        template = "comment/magazine.html"

    # 获取评测所属游戏
    for item in current_page_data.object_list:
        shelf = Shelf.objects.filter(gameId=item.gameId).first()
        if shelf is not None:
            shelf.cover = shelf.cover.replace("\'", "\"")
            cover = json.loads(shelf.cover, encoding="utf-8")[0]
            item.__setattr__("shelf_cover", cover)
        else:
            item.__setattr__("shelf_cover", "/static/image/ns.png")

    page_range = range(1, page_count+1)
    if page_count > 6:
        page_range = range(1, 6+1)
    if current_page_data.number > 3:
        page_range = range(current_page_data.number - 3, current_page_data.number + 3)

    render_data = {
        "active": active,
        "list": current_page_data.object_list,
        "page_count": page_count,
        "page_range": page_range,
        "current_page": current_page_data,
        "magzines": mag_obj.getMagzineNames(),
    }
    # print(render_data["list"])
    # return HttpResponse("ooo")
    return render(request, template, render_data)


# 根据游戏id获取评测
def review(request, pk):
    current_action = "review"

    if pk != 0:
        review = MagzineScores.objects.filter(id=pk).first()
        game = None
        if review.gameId != 0:
            game = Shelf.objects.filter(gameId=review.gameId).first()
            game.cover = json.loads(game.cover.replace("\'", "\""))[0]

        render_data = {
            "active": active,
            "review": review,
            "game": game,
            "breadcrumb": breadcrumb(current_action, gameId=review.gameId)
        }

        if theme == "weui":
            template = "weui/review/game.html"
        else:
            template = "comment/review.html"

        return render(request, template, render_data)
    else:
        return HttpResponse("请求的游戏ID不存在！")


# 用户评分（@TODO）
def member(request):
    pass