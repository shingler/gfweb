#!/usr/bin/python
# -*- coding:utf-8 -*-
# 修改个人资料
from django.contrib.auth import login
from ossManager.manager import OssTokenManager
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.http.response import JsonResponse


@login_required(login_url="/")
def index(request):
    # 当前登录用户信息
    userObj = request.user
    # 头像直传token
    token_manager = OssTokenManager()
    oss_token = token_manager.get_token("avatar", prefix="avatar")

    data = {"profile": userObj, "oss_token": oss_token}
    return render(request, "weui/siginin/profile.html", data)


# 修改用户名
def changeusername(request):
    # print(request.POST)
    new_name = request.POST.get("newname")
    # 保存新的用户名
    request.user.username = new_name
    if request.user.save():
        request.user.userprofile.nickname = new_name
        request.user.userprofile.save()
        res = {
            "status": 1,
            "msg": "保存成功",
            "new_name": request.POST.get("newname")
        }
    else:
        res = {
            "status": 0,
            "msg": "保存失败"
        }
    return JsonResponse(res)


# 修改头像
def changeavatar(request):
    avatar = request.POST.get("avatar_path")
    request.user.userprofile.avatar = avatar
    request.user.userprofile.save()
    return JsonResponse({"status": 1, "msg": "ok", "data": {"avatar": avatar}})


# 头像修改token
def avatartoken(request):
    # 头像直传token
    token_manager = OssTokenManager()
    # @TODO 指定头像文件的key
    oss_token = token_manager.get_token("avatar", prefix="avatar")
    return JsonResponse(oss_token, safe=False)
