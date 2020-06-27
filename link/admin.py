import time

from django.contrib import admin

# Register your models here.
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.core.paginator import PageNotAnInteger, EmptyPage, Paginator
from GameModel.models import Shelf, Subjects, MagzineScores, Platforms
from gfweb import translate
import numpy
from django.contrib import admin
from . import util
import json
import logging

# 面包屑导航
from link.models import Link

breadcrumb = {
    "游戏列表": "myadmin.game.list",
}

# 图标列表
icons = {
    "ps4": "image/ps4.png",
    "switch": "image/switch.png"
}
logger = logging.getLogger("gfweb.debug")


@admin.register(Link)
class LinkAdmin(admin.ModelAdmin):

    # 游戏列表
    def list(request, page=1, *args, **kwargs):
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
            # 取第一张封图和第一张截图判断是否已转存oss
            is_save_to_oss = True
            if len(s.cover) > 0 and s.cover[0].startswith("http"):
                is_save_to_oss = False

            s.thumb = json.loads(json.dumps(eval(s.thumb)), encoding="utf-8")
            if len(s.thumb) > 0 and s.thumb[0].startswith("http"):
                is_save_to_oss = False
            s.__setattr__("is_save_to_oss", is_save_to_oss)

        pagitor = Paginator(sub_list, size)
        try:
            current_page = pagitor.page(page)
        except EmptyPage:
            current_page = pagitor.page(pagitor.num_pages)
        except PageNotAnInteger:
            current_page = pagitor.page(1)

        render_data = {
            "pagitor": current_page,
            "breadcrumb": breadcrumb,
            "icons": icons
        }
        return render(request, "myadmin/list.html", render_data)

    # 游戏信息关联
    def link(request):
        # 添加或修改
        if request.method == 'POST':
            ps4_ids = []
            switch_ids = []
            linked = []
            if "linked" in request.POST:
                linked = request.POST.getlist("linked")
            if "game_ids" in request.POST:
                game_ids = request.POST.getlist("game_ids")

            gameIds = numpy.hstack((game_ids, linked))
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
            logger.debug("未翻译，用时:%d" % int(time.process_time()))

            if "hk" not in intro:
                intro["trans"] = translate.translate(list(intro.values())[0])
                logger.debug("执行翻译后，用时:%d" % int(time.process_time()))

            shelf.intro = json.dumps(intro, ensure_ascii=False)
            if shelf.language.find("中文"):
                shelf.hasChinese = True

            shelf.save()

            # 保存了之后，将subject的onShelf改成1
            for s in games:
                s.onShelf = True
                s.save()
            logger.debug("已保存数据，用时:%d" % int(time.process_time()))

            # v 1.1.0 将转存改为异步处理

            return HttpResponseRedirect("/admin/refer/list")

        else:
            shelf = None
            if "game_id" in request.GET:
                shelf = Shelf.objects.get(gameId=request.GET["game_id"])
                if shelf is not None and shelf.officialGameIds != "":
                    sub_list = Subjects.objects.filter(officialGameId__in=shelf.officialGameIds.split(','))
                    print(shelf.officialGameIds, sub_list)
                    shelf.__setattr__("sub_list", sub_list)

            # 读取platforms信息。游戏列表从ajax接口读取
            platforms = Platforms.objects.order_by("-platform").order_by("countryArea").all()

            # 面包屑
            breadcrumb["关联游戏"] = ""

            render_data = {
                "list": platforms,
                "shelf": shelf,
                "breadcrumb": breadcrumb
            }

            return render(request, "myadmin/link.html", render_data)

    # 关联媒体评测
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
            # print(score_ids, mag_ids)
            scores = []
            for mid in mag_ids:
                # 将不再勾选的文章撤掉关联
                mag_remove = MagzineScores.objects.filter(gameId=game_id)
                for mr in mag_remove:
                    if str(mr.id) not in mag_ids:
                        # print(mr.id, mag_ids)
                        mr.gameId = 0
                        mr.save()

                # 关键游戏ID，翻译评价原文
                mag = MagzineScores.objects.get(id=mid)
                mag.gameId = game_id
                if mag.magazine != "IGN" and len(mag.comment) > 0 and len(mag.comment_trans) == 0:
                    mag.comment_trans = translate.translate(mag.comment)
                mag.save()

                # meta网站是百分制
                the_score = mag.score if mag.score <= 10 else mag.score / 10
                scores.append(the_score)
            # 更新评分
            shelf.score = sum(scores) / len(scores)
            shelf.save()

        # 加载已关联的游戏评测
        mags = MagzineScores.objects.filter(gameId=game_id)
        if mags:
            shelf.__setattr__("mags", mags)

        # 加载评测媒体名
        magazines = MagzineScores.MAG_CHOICE

        # 面包屑
        breadcrumb["关联评测"] = ""

        render_data = {
            "shelf": shelf,
            "magazines": magazines,
            "breadcrumb": breadcrumb
        }

        return render(request, "myadmin/magzine.html", render_data)

    # 删除关联数据
    def unlink(request, game_id=0):
        shelf = Shelf.objects.get(gameId=game_id)
        if shelf is None:
            return JsonResponse({"status": 0, "msg": "不存在的数据"})

        # shelf.delete()
        # 改成软删除，设置show=0
        shelf.show = False
        shelf.save()
        return JsonResponse({"status": 1, "msg": "删除成功"})

    # 图片转存OSS
    def picture(request, game_id=0):
        if game_id != 0:
            # 保存了之后，将图片上传到oss，并更新
            # 上传到oss并获得路径
            game_obj = Shelf.objects.get(gameId=game_id)
            if game_obj:
                om = util.OssManager()

                # 转存封图逻辑（暂只转存第一张，反正也只显示一张而已）
                # 先判断封图是否已转存
                covers = json.loads(game_obj.cover.replace('\'', '\"'))
                cover_bucket = 'cover'
                if len(covers) > 0 and covers[0].startswith("http"):
                    oss_covers = []
                    for c in covers[:1]:
                        # 通过域名判断是否已转存
                        try:
                            oss_covers.append(om.upload(cover_bucket, c, game_obj.gameId))
                        except util.OssException as ex:
                            print(ex)
                        except Exception as ex:
                            print(ex)
                    game_obj.cover = json.dumps(oss_covers)
                    game_obj.save()

                # 转存截图逻辑（暂只转前8张，多了会导致504）
                # 先判断截图是否已转存
                thumb = json.loads(game_obj.thumb.replace('\'', '\"'))
                thumb_bucket = 'thumb'
                if len(thumb) > 0 and thumb[0].startswith("http"):
                    oss_thumb = []
                    for t in thumb[:8]:
                        try:
                            oss_thumb.append(om.upload(thumb_bucket, t, game_obj.gameId))
                        except util.OssException as ex:
                            print(ex)
                        except Exception as ex:
                            print(ex)

                    game_obj.thumb = json.dumps(oss_thumb)
                    game_obj.save()

                debug = "将图片保存至OSS，用时:%f" % time.process_time()
                print(debug)
                logger.debug(debug)
                return JsonResponse({"status": 1, "msg": "转存成功"})
            else:
                return JsonResponse({"status": 0, "msg": "不存在的游戏"})
        else:
            return JsonResponse({"status": 0, "msg": "非法请求"})

    def changelist_view(self, request, extra_context=None):
        return self.list(request)

    # json格式游戏列表数据
    def game_list(request):
        platform = request.GET["platform"].lower()
        saleArea = request.GET["saleArea"].lower()
        subject_list = Subjects.objects.filter(platform=platform, saleArea=saleArea, onShelf=False) \
            .order_by("officialGameId").values("officialGameId", "subject", "url")
        return JsonResponse(list(subject_list), safe=False, json_dumps_params={'ensure_ascii': False})

    # json格式评测数据
    def review_list(request):
        magazine = request.GET["magazine"].lower()
        review_list = MagzineScores.objects.filter(gameId=0, magazine=magazine) \
            .order_by("subject").values("id", "subject", "score", "url")
        return JsonResponse(list(review_list), safe=False, json_dumps_params={'ensure_ascii': False})
