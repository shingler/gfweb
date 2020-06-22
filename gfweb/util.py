#!/usr/bin/python
# -*- coding:utf-8 -*-

# 图标列表
icons = {
    "ps4": "image/ps4.png",
    "switch": "image/switch.png",
}
logo = {
    "Famitsu": "image/famitsu.png",
    "metacritic": "image/metacritic.png",
    "gamespot": "image/gamespot.png",
}

# 按比例拆分列表
def split_list(lst, n):
    return [lst[i:i+n] for i in range(0, len(lst), n)]


# 定义面包屑导航
def breadcrumb(current_action, platform="all", gameId=0, magId=0):
    crumb = [
        {
            "action": "list",
            "url_name": "list",
            "label": "游戏列表",
            "active": False,
            "param": platform
        },
        {
            "action": "detail",
            "url_name": "detail",
            "label": "游戏详情",
            "active": False,
            "param": gameId
        },
        {
            "action": "review",
            "url_name": "magazine.review",
            "label": "游戏评测",
            "active": False,
            "param": magId
        },
    ]

    i = 0
    for k, v in enumerate(crumb):
        if v["action"] == current_action:
            i = k

    result = crumb[:i+1]
    result[i]["active"] = True
    print(result)
    return result
