import time

from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render
from django.http.response import JsonResponse

from gfweb import util
from favorite.models import Favorite


# 添加收藏
def add(request, game_id=0):
    res = {
        "status": 0,
        "msg": "",
        "data": {}
    }
    if not game_id:
        res["status"] = 0
        res["msg"] = "无效请求"
        return JsonResponse(res)

    if not request.user.is_authenticated:
        res["status"] = 0
        res["msg"] = "请先登录"
        return JsonResponse(res)

    favObj = Favorite.objects.filter(user_id=request.user.id, shelf_id=game_id).first()
    if favObj:
        favObj.state = 1
        favObj.updated = time.time()
        favObj.save()
    else:
        favObj = Favorite()
        favObj.user_id = request.user.id
        favObj.shelf_id = game_id
        favObj.state = 1
        favObj.created = time.time()
        favObj.updated = time.time()
        favObj.save()
    res["status"] = 1
    res["msg"] = "操作成功"
    res["data"] = {"state": favObj.state}
    return JsonResponse(res)


# 取消收藏
def remove(request, game_id=0):
    res = {
        "status": 0,
        "msg": "",
        "data": {}
    }
    if not game_id:
        res["status"] = 0
        res["msg"] = "无效请求"
        return JsonResponse(res)

    if not request.user.is_authenticated:
        res["status"] = 0
        res["msg"] = "请先登录"
        return JsonResponse(res)

    favObj = Favorite.objects.filter(user_id=request.user.id, shelf_id=game_id).first()
    if not favObj:
        res["status"] = 0
        res["msg"] = "还没有收藏呢，亲"
        return JsonResponse(res)

    favObj.state = 0
    favObj.updated = time.time()
    favObj.save()

    res["status"] = 1
    res["msg"] = "操作成功"
    res["data"] = {"state": favObj.state}
    return JsonResponse(res)


# 收藏列表
@login_required(login_url="/")
def list(request):
    user_id = request.user.id
    list = Favorite.objects.filter(user_id=user_id, state=True).order_by("-updated")
    # 分页
    page = request.GET.get("page", default=1)
    paginator = Paginator(list, per_page=10)
    try:
        current_page_data = paginator.page(page)
    except PageNotAnInteger:
        current_page_data = paginator.page(1)
    except EmptyPage:
        current_page_data = paginator.page(paginator.num_pages)

    # 控制页码范围
    page_range = range(1, paginator.num_pages + 1)
    if paginator.num_pages > 6:
        page_range = range(1, 6 + 1)
    if current_page_data.number > 3:
        page_range = range(current_page_data.number - 3, current_page_data.number + 3)

    render_data = {
        "current_page": current_page_data,
        "page_range": page_range,
        "current_user": request.user,
        "icons": util.icons
    }
    return render(request, "weui/favorite/list.html", render_data)

