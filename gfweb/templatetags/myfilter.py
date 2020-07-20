#!/usr/bin/python
# -*- coding:utf-8 -*-
import json

from django import template
from django.middleware import csrf
from ossManager import manager
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
    return d.get(key)

# 自动加oss域名并兼容外站链接
@register.filter(name="show_pic")
def show_pic(url, param=''):
    # print(url, type(url))
    if url is None:
        return "/static/image/loading.gif"
    if url.startswith('http') or len(param) == 0:
        # 外站图片直接展示
        return url
    else:
        # 阿里云oss图片，可以进一步处理
        params = param.split(',')
        # print(params)
        om = manager.OssManager()
        if len(params) > 1:
            return om.get_url(url, params[0], params[1])
        else:
            return om.get_url(url, params[0])

# 获取csrf_token
@register.filter(name="get_csrf")
def get_csrf(request):
    return csrf.get_token(request)

# 封图是否已转存
@register.filter(name="if_save_to_oss")
def if_save_to_oss(url):
    return not url.startswith("http")

# 判断登录状态
@register.filter(name="is_login")
def is_login(request):
    # print(request.user.userprofile.avatar)
    return request.user.is_authenticated

# 将可序列化的字符转存json
@register.filter(name="to_json")
def to_json(json_str):
    # 单双引号兼容
    json_str = json_str.replace('\'', '\"')
    try:
        res = json.loads(json_str, encoding="utf-8")
    except Exception as err:
        print(err)
        res = json_str
    # print(res)
    return res
