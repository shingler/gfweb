#!/usr/bin/python
# -*- coding:utf-8 -*-
import json
import time

from django.shortcuts import render
from GameModel.models import Currency, MagzineScores, Shelf, Subjects
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .util import *

active = "games"
theme = "weui"

# 游戏列表页
def list(request, platform="all", page=1):
    size = 20
    kw = False

    # 关键词搜索
    if "kw" in request.GET and request.GET["kw"] != "":
        kw = request.GET["kw"]
        list = Shelf.objects.filter(keyword__icontains=kw).order_by("-gameId")
    elif platform == "all":
        list = Shelf.objects.all().order_by("-gameId")
    else:
        list = Shelf.objects.filter(platform=platform).order_by("-gameId")

    for s in list:
        # 兼容单引号json串。明明也是python生成的，竟然会出现单引号，奇怪
        s.cover = json.loads(json.dumps(eval(s.cover)), encoding="utf-8")
        try:
            intro = json.loads(json.dumps(eval(s.intro)), encoding="utf-8")
            if "hk" in intro:
                s.intro = intro["hk"]
            elif "trans" in intro:
                s.intro = intro["trans"]
            # 去掉PSN游戏介绍里的copyright信息
            if s.intro.find("<b>Copyright：</b>") > 0:
                s.intro = s.intro[0:s.intro.find("<b>Copyright：</b>")]
        except:
            pass

    # 使用内置分页器
    p = Paginator(list, size)
    try:
        current_page_data = p.page(page)
    except PageNotAnInteger:
        current_page_data = p.page(1)
    except EmptyPage:
        current_page_data = p.page(p.num_pages)

    template_path = "weui/games/list.html"

    if theme == "bootstrap":
        # weui每行数量固定，所以对数据做均等拆分
        obj_list = current_page_data.object_list
        current_page_data.object_list = split_list(obj_list, 4)
        template_path = "bootstrap/games/list.html"

    render_data = {
        'page_obj': current_page_data,
        'platform': platform,
        'active': active,
        'kw': kw,
        "icons": icons
    }

    return render(request, template_path, render_data)


# 游戏详情页
def detail(request, game_id=0):
    current_action = "detail"

    info = Shelf.objects.get(gameId=game_id)
    rate_update = 0
    if info is not None:
        price = Subjects.objects.filter(officialGameId__in=info.officialGameIds.split(','))
        # 货币转换
        # curr = Currency()
        for p in price:
            (rate_price, updated) = Currency.getLatestAmount(p.currency, p.latestPrice)
            if rate_price:
                p.__setattr__("latestPriceCNY", rate_price)
                rate_update = time.strftime("%Y年%m月%d日", time.localtime(updated))

        info.__setattr__("price", price)
        info.cover = json.loads(json.dumps(eval(info.cover)))
        # 截图最多展示8张（后台只转存最多8张）
        info.thumb = json.loads(json.dumps(eval(info.thumb)))[:8]
        try:
            # 兼容非json格式
            intro = json.loads(json.dumps(eval(info.intro)))
            if "hk" in intro:
                info.intro = intro["hk"]
            elif "trans" in intro:
                info.intro = intro["trans"]
            # 去掉PSN游戏介绍里的copyright信息
            if info.intro.find("<b>Copyright：</b>") > 0:
                info.intro = info.intro[0:info.intro.find("<b>Copyright：</b>")]
        except:
            pass
    # 获取评测
    score = MagzineScores.objects.filter(gameId=game_id)

    # 图片轮播（优先取截图，无截图用封图）
    # carousel = info.thumb if len(info.thumb) > 0 else info.cover
    carousel = info.thumb

    render_data = {
        'info': info, 'score': score, 'active': active, 'logo': logo,
        'rate_update': rate_update, 'carousel': carousel,
        'icons': icons, 'breadcrumb': breadcrumb(current_action, gameId=game_id)
    }
    print(render_data["breadcrumb"])

    if theme == "bootstrap":
        template = "games/detail.html"
    else:
        template = "weui/games/detail.html"
    return render(request, template, render_data)


# 搜索页
def search(request):
    template = "weui/games/search.html"
    render_data = {
        'active': 'search'
    }
    return render(request, template, render_data)
