#!/usr/bin/python
# -*- coding:utf-8 -*-
# oss配置

OSS_ACCESS_KEY_ID = 'LTAI4G2XhHM468ZgT6Kv5Fwp'
OSS_ACCESS_KEY_SECRET = 'IKeRVtMlZ9n0vUQvngSVWPyyPzHIEl'
OSS_END_POINT = 'http://oss-cn-beijing.aliyuncs.com'

# bucket设置 {类别/用途:{bucket:BUCKET, domain:域名, style:[STYLE]}
OSS_BUCKETNAME = {
    # 封图
    "cover": {"bucket": 'gf-cover', "domain": "gf-cover.oss-cn-beijing.aliyuncs.com",
              "style": ["list_icon_w200", "list_icon_w400", "detail_pic_w500",
                        "mp_list_icon_w60h60", "mp_detail_pic_w414"]},
    # 截图
    "thumb": {"bucket": 'gf-thumb', "domain": "gf-thumb.oss-cn-beijing.aliyuncs.com",
              "style": ["detail_pic_w500", "mp_detail_pic_w414h240"]},
    # 头像
    "avatar": {"bucket": 'gf-avatar', "domain": "gf-avatar.oss-cn-beijing.aliyuncs.com",
               "style": ["avatar_middle_w80h80"]},
}
