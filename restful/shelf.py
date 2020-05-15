#!/usr/bin/python
# -*- coding:utf-8 -*-
from GameModel import models


def getSubjects(officialGameIds):
    subjects = models.Subjects.objects.filter(officialGameId__in=officialGameIds).order_by("-id")
    return subjects


class Shelf(models.Shelf):
    pass
