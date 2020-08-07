#!/usr/bin/python
# -*- coding:utf-8 -*-
from django.urls import path
from favorite import views

# 收藏页面
urlpatterns = [
    path('add/<game_id>', views.add, name="favorite-add"),
    path('remove/<game_id>', views.remove, name="favorite-remove"),
    path('list', views.list, name="favorite-list"),
]
