#!/usr/bin/python
# -*- coding:utf-8 -*-
from django.urls import path
from link.admin import LinkAdmin

urlpatterns = [
    path('list', LinkAdmin.list, name="myadmin.game.list"),
    path('list/<int:page>', LinkAdmin.list, name="myadmin.game.list"),
    path('link/', LinkAdmin.link, name="myadmin.game.link"),
    path('magzine/<game_id>/', LinkAdmin.magzine, name="myadmin.game.magzine"),
    path('game_list', LinkAdmin.game_list, name="myadmin.game.list.ajax"),
    path('review_list', LinkAdmin.review_list, name="myadmin.review.list.ajax"),
    path('list/unlink/<game_id>', LinkAdmin.unlink, name="myadmin.game.link.unlink"),
    path('link/picture/<game_id>', LinkAdmin.picture, name="myadmin.game.link.picture"),
]
