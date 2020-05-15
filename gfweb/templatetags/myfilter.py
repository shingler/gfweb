#!/usr/bin/python
# -*- coding:utf-8 -*-
from django import template
register = template.Library()

# 获取循环范围
@register.filter
def get_range(n):
    return range(n)

# 分割字符串
@register.filter
def split(str, sep=','):
    return str.split(sep)

# 访问字典
@register.filter
def get_item(d, key):
    return d[key]
