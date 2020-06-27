#!/usr/bin/python
# -*- coding:utf-8 -*-
# 评分/评论页面
import json
import math

from django.http.response import HttpResponse, HttpResponseRedirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render
from GameModel.models import MagzineScores, Shelf, Magazines
from .util import *

active = "comment"
theme = "weui"


# 首页
def home(request):
    # 每个杂志一块，每块显示评分Top4的游戏
    magazines = Magazines.objects.filter(enable=True)
    data = {}
    review_ids = []
    for m in magazines:
        top4 = MagzineScores.objects.filter(magazine=m.title, gameId__gt=0).order_by("-score")[:4]
        data[m.title] = top4
        review_ids += map(lambda x: x.gameId, top4)

    # 获取评测的游戏标题、封图等
    games = Shelf.objects.filter(gameId__in=review_ids).only("gameId", "cover", "titleCh")

    # 游戏信息和杂志块发生关联
    game_cover = {}
    for game in games:
        game_cover[game.gameId] = json.loads(game.cover.replace('\'', '\"'), encoding="utf-8")[0]
    print(logo)
    # 评测信息和游戏信息不必捏合到一起，通过gameId可以访问game_data里的数据
    render_data = {
        "active": active, "magazines": data, "game_cover": game_cover,
        "logo": logo
    }
    return render(request, "weui/review/home.html", render_data)
    # return HttpResponse("test")


# 媒体评分
def magazine(request, magazine=""):
    # request数据
    get_data = request.GET.copy()
    page = get_data.setdefault("page", 1)

    # 根据游戏名查找评分 @TODO
    game_name = get_data.setdefault("g", "")
    # 根据得分范围查找评分 @TODO
    score_low = get_data.setdefault("low", 1)
    score_high = get_data.setdefault("high", 10)

    # 获取数据
    size = 10
    filters = {"gameId__gt": 0}
    if len(magazine):
        filters["magazine"] = magazine
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

    template = "weui/review/magazine.html"
    if theme == "bootstrap":
        template = "bootstrap/comment/magazine.html"

    # 获取评测所属游戏
    for item in current_page_data.object_list:
        shelf = Shelf.objects.filter(gameId=item.gameId).first()
        if shelf is not None:
            shelf.cover = shelf.cover.replace("\'", "\"")
            cover = json.loads(shelf.cover, encoding="utf-8")[0]
            item.__setattr__("shelf_cover", cover)
        else:
            item.__setattr__("shelf_cover", "/static/image/ns.png")

    page_range = range(1, paginator.num_pages+1)
    if paginator.num_pages > 6:
        page_range = range(1, 6+1)
    if current_page_data.number > 3:
        page_range = range(current_page_data.number - 3, current_page_data.number + 3)

    render_data = {
        "active": active,
        "list": current_page_data.object_list,
        "page_count": paginator.num_pages,
        "page_range": page_range,
        "current_page": current_page_data,
        "magzines": mag_obj.getMagzineNames(),
        "logo": logo,
    }

    return render(request, template, render_data)


# 根据游戏id获取评测
def review(request, pk):
    current_action = "review"

    if pk != 0:
        review = MagzineScores.objects.filter(id=pk).first()
        game = None
        if review.gameId != 0:
            game = Shelf.objects.filter(gameId=review.gameId).first()
            # 如果数据库里没有关联或gameId查不到，跳转到原url吧。。。
            if game is None:
                return HttpResponseRedirect(review.url)
            
            game.cover = json.loads(game.cover.replace("\'", "\""))[0]

        render_data = {
            "active": active,
            "review": review,
            "game": game,
            "breadcrumb": breadcrumb(current_action, gameId=review.gameId),
            "logo": logo,
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