#!/usr/bin/python
# -*- coding:utf-8 -*-
import json

from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.core.paginator import PageNotAnInteger, EmptyPage, Paginator
from GameModel.models import Shelf, Subjects, MagzineScores
from gfweb import translate
import numpy
from django.contrib import admin

# 面包屑导航
breadcrumb = {
    "游戏列表": "myadmin.game.list",
}


class LinkAdmin(admin.ModelAdmin):

    def list(request, page=1):
        # 检查登录
        print(request.user.username)
        if not request.user:
            return HttpResponseRedirect("/admin/", )

        size = 10
        sub_list = Shelf.objects.all().order_by("-gameId")
        # 解json
        for s in sub_list:
            # 兼容单引号json串。明明也是python生成的，竟然会出现单引号，奇怪
            s.cover = json.loads(json.dumps(eval(s.cover)), encoding="utf-8")
        pagitor = Paginator(sub_list, size)
        try:
            current_page = pagitor.page(page)
        except EmptyPage:
            current_page = pagitor.page(pagitor.num_pages)
        except PageNotAnInteger:
            current_page = pagitor.page(1)

        render_data = {
            "pagitor": current_page,
            "breadcrumb": breadcrumb
        }
        return render(request, "myadmin/list.html", render_data)

    def link(request):
        # 添加或修改
        if request.method == 'POST':
            ps4_ids = []
            switch_ids = []
            linked = []
            if "linked" in request.POST:
                linked = request.POST.getlist("linked")
            if "ps4-games" in request.POST:
                ps4_ids = request.POST.getlist("ps4-games")
            if "switch-games" in request.POST:
                switch_ids = request.POST.getlist("switch-games")
            gameIds = numpy.hstack((ps4_ids, switch_ids, linked))
            # print(gameIds)
            games = Subjects.objects.filter(officialGameId__in=gameIds)
            shelf = Shelf()
            if "gameId" in request.POST and request.POST["gameId"] != "":
                shelf.gameId = request.POST["gameId"]

            shelf.officialGameIds = ",".join(gameIds)
            shelf.show = request.POST["show"]
            # shelf.show = 1
            shelf.titleCh = request.POST["title"]
            shelf.keyword = request.POST["keyword"].replace('\r\n', ' ')
            # 从subject中提取汇总数据
            covers = []
            thumb = []
            video = []
            platform = []
            keywords = []
            intro = {}

            if games:
                for s in games:
                    # 更新语言标题
                    if s.saleArea.lower() == "jp":
                        shelf.titleJp = s.subject
                    elif s.saleArea.lower() in ("us", "za"):
                        shelf.titleEn = s.subject
                    if s.saleArea.lower() == "hk" and len(request.POST["title"]) == 0:
                        shelf.titleCh = s.subject
                    # 合并各个语言的介绍 格式：JSON
                    # shelf.intro += s.intro + "\r\n\r\n"
                    intro[s.saleArea.lower()] = s.intro
                    # 合并封图，截图和视频
                    covers.append(s.cover)
                    if len(s.thumb) > 0:
                        # print(thumb, json.loads(s.thumb, encoding="UTF-8"))
                        thumb += json.loads(s.thumb, encoding="UTF-8")
                        # print(thumb)
                    if len(s.video) > 0:
                        video += json.loads(s.video, encoding="UTF-8")
                    # 合并语言版本，更新游玩人数
                    shelf.language += s.edition + ","
                    shelf.players = s.players
                    platform.append(s.platform)
                    # 将每个版本游戏名保存为关键词
                    keywords += s.subject.split(" ")

            keywords += request.POST["title"].split(" ")
            # 过滤空格和冒号等符号
            keyword_list = set(keywords)
            for kw in set(keywords):
                if kw.strip() == "" or kw == ":":
                    keyword_list.remove(kw)
            shelf.keyword += " ".join(keyword_list)
            shelf.cover = json.dumps(covers)
            shelf.thumb = json.dumps(thumb)
            shelf.video = json.dumps(video)
            shelf.platform = ",".join(set(platform))
            # 无中文介绍，翻译
            if "hk" not in intro:
                intro["trans"] = translate.translate(list(intro.values())[0])

            shelf.intro = json.dumps(intro, ensure_ascii=False)
            if shelf.language.find("中文"):
                shelf.hasChinese = True
            # 保存了之后，将subject的onShelf改成1
            shelf.save()
            for s in games:
                s.onShelf = True
                s.save()

            return HttpResponseRedirect("/admin/refer/list")

        else:
            shelf = None
            if "game_id" in request.GET:
                shelf = Shelf.objects.get(gameId=request.GET["game_id"])
                if shelf is not None and shelf.officialGameIds != "":
                    sub_list = Subjects.objects.filter(officialGameId__in=shelf.officialGameIds.split(','))
                    print(shelf.officialGameIds, sub_list)
                    shelf.__setattr__("sub_list", sub_list)

            ps4_hk_list = Subjects.objects.filter(platform="ps4", saleArea="hk", onShelf=False).order_by("officialGameId")
            switch_jp_list = Subjects.objects.filter(platform="switch", saleArea="jp", onShelf=False).order_by(
                "officialGameId")
            switch_us_list = Subjects.objects.filter(platform="switch", saleArea="us", onShelf=False).order_by(
                "subject")
            switch_hk_list = Subjects.objects.filter(platform="switch", saleArea="hk", onShelf=False).order_by(
                "officialGameId")
            switch_za_list = Subjects.objects.filter(platform="switch", saleArea="za", onShelf=False).order_by(
                "subject")

            # 面包屑
            breadcrumb["关联游戏"] = ""

            render_data = {
                "ps4_list": {
                    "香港": ps4_hk_list,
                },
                "switch_list": {
                    "香港": switch_hk_list, "日本": switch_jp_list,
                    "美国": switch_us_list, "南非": switch_za_list
                },
                "shelf": shelf,
                "breadcrumb": breadcrumb
            }

            return render(request, "myadmin/link.html", render_data)

    def magzine(request, game_id=0):
        if game_id == 0:
            return HttpResponseRedirect("/admin/refer/list")

        shelf = Shelf.getData(game_id)

        # 关联评测
        if request.method == "POST":
            # 新勾选的评测文章
            article_ids = request.POST.getlist("articles")
            # 已勾选的评测文章
            score_ids = request.POST.getlist("score_id")
            # 新旧文章合并
            mag_ids = numpy.hstack((score_ids, article_ids))
            # print(mag_ids)
            scores = []
            for mid in mag_ids:
                # 关键游戏ID，翻译评价原文
                mag = MagzineScores.objects.get(id=mid)
                mag.gameId = game_id
                if mag.magazine != "IGN" and len(mag.comment) > 0:
                    mag.comment_trans = translate.translate(mag.comment)
                mag.save()
                # meta网站是百分制
                the_score = mag.score if mag.score <= 10 else mag.score / 10
                scores.append(the_score)
            # 更新评分
            shelf.score = sum(scores) / len(scores)
            shelf.save()

        # 加载游戏评测
        mags = MagzineScores.objects.filter(gameId=game_id)
        if mags:
            shelf.__setattr__("mags", mags)
        # 加载所有评测
        ign = MagzineScores.objects.filter(magazine="IGN", gameId=0).order_by("subject")
        gamespot = MagzineScores.objects.filter(magazine='gamespot', gameId=0).order_by("subject")
        metacritic = MagzineScores.objects.filter(magazine='metacritic', gameId=0).order_by("subject")
        famitsu = MagzineScores.objects.filter(magazine='famitsu', gameId=0).order_by("subject")

        # 面包屑
        breadcrumb["关联评测"] = ""

        render_data = {
            "shelf": shelf,
            "magzine": {
                "ign": ign, "gamespot": gamespot, "metacritics": metacritic, "famitsu": famitsu
            },
            "breadcrumb": breadcrumb
        }
        return render(request, "myadmin/magzine.html", render_data)

    actions = [list,]
    actions_on_top = True

    def get_actions(self, request):
        actions = super(LinkAdmin, self).get_actions(request)
        print(request.user.username)
