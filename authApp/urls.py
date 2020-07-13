#!/usr/bin/python
# -*- coding:utf-8 -*-
from django.urls import path

from authApp import signin

urlpatterns = [
    path('signin/alipay/authorize', signin.alipay.authorize, name="sigin-alipay-authorize"),
    path('signin/alipay/token', signin.alipay.token, name="signin-alipay-token"),
    path('signin/logout', signin.connect.logout, name="sigin-logout"),
]