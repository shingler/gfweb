#!/usr/bin/python
# -*- coding:utf-8 -*-
from django.conf.urls import url, include
from rest_framework import routers

from restful import views

app_name = "restful"

router = routers.DefaultRouter
# router.register(prefix=r'games', viewset=views.ShelfViewSet)
router.register(r'games', views.ShelfViewSet)
router.register(r'magzine', views.MagzineViewSet)
router.register(r'subject', views.SubjectsViewSet)

urlpatterns = [
    url(r'^api/subject/(?P<officialGameId>[0-9a-zA-Z\-_]+)$', views.SubjectsViewSet.retrieve, name="subject-list"),
    url(r'^api/', include(router.urls)),
]


