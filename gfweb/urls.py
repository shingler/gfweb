"""gfweb URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf.urls import re_path, url

import authApp.urls
import link.urls
import favorite.urls
from gfweb import games, comment
from restful import views
from rpc4django.views import serve_rpc_request
from rest_framework import routers
from rest_framework.schemas import get_schema_view

app_name = "gfweb"

# rest router
router = routers.DefaultRouter()
router.register(r'games', views.ShelfViewSet)
router.register(r'magzine', views.MagzineViewSet)
router.register(r'subject', views.SubjectsViewSet)

# schema
schema_view = get_schema_view(title="Game Finder API")

urlpatterns = [
    # django 默认的管理地址
    path('admin/', admin.site.urls),

    # 首页
    path('', games.list, name="list"),

    # 前端展示页面
    re_path(r'^games/list/(?P<platform>\w*)/$', games.list, name="list"),
    # re_path(r'^games/list/(?P<platform>\w*)/(?P<page>\d?)/$', games.list, name="list.page"),
    path('games/info/<game_id>/', games.detail, name="detail"),

    # 媒体评测
    path('comment/', comment.home, name="magazine.home"),
    path('comment/magazine/<magazine>', comment.magazine, name="magazine.list"),
    url(r'^comment/magazine/(?P<pk>[0-9]+)/$', comment.review, name="magazine.review"),

    # 搜索页
    path('games/search', games.search, name="search"),

    # rpc4django will need to be in your Python path
    url(r'^RPC2$', serve_rpc_request),

    # restful接口
    url(r'^api/subject/(?P<officialGameId>[0-9a-zA-Z\-_]+)$', views.SubjectsViewSet.retrieve, name="subject-list"),
    url(r'^api/magzine/game/list$', views.MagzineViewSet.list, name="magzine-list"),
    url(r'^api/', include(router.urls)),
    # schema
    url(r'^schema/$', schema_view),

    # 游戏关联模块
    path('admin/refer/', include(link.urls)),

    # 登录认证模块
    path('auth/', include(authApp.urls)),

    # 收藏模块
    path('fav/', include(favorite.urls)),
]

