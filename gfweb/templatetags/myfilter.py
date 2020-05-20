#!/usr/bin/python
# -*- coding:utf-8 -*-
from django import template
from link import util
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

# 自动加oss域名并兼容外站链接
@register.filter(name="show_pic")
def show_pic(url, param=''):
    if url.startswith('http') or len(param) == 0:
        # 外站图片直接展示
        return url
    else:
        # 阿里云oss图片，可以进一步处理
        params = param.split(',')
        print(params)
        om = util.OssManager()
        if len(params) > 1:
            return om.get_url(url, params[0], params[1])
        else:
            return om.get_url(url, params[0])
