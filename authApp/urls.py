#!/usr/bin/python
# -*- coding:utf-8 -*-
from django.urls import path

from authApp import signin, profile

urlpatterns = [
    path('signin/alipay/authorize', signin.alipay.authorize, name="sigin-alipay-authorize"),
    path('signin/alipay/token', signin.alipay.token, name="signin-alipay-token"),
    path('signin/logout', signin.connect.logout, name="sigin-logout"),
    # 个人资料
    path('profile', profile.index, name="profile-index"),
    path('changeusername', profile.changeusername, name="change-username"),
    path('changeavatar', profile.changeavatar, name="change-avatar"),
]