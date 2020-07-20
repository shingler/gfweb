#!/usr/bin/python
# -*- coding:utf-8 -*-
# oss配置

OSS_ACCESS_KEY_ID = 'YOUR ALIYUN OSS ACCESS KEY ID'
OSS_ACCESS_KEY_SECRET = 'YOUR ALIYUN OSS ACCESS KEY SECRET'
OSS_END_POINT = 'YOUR ALIYUN OSS BUCKET ENDPOINT'

# bucket设置 {类别/用途:{bucket:BUCKET, domain:域名, style:[STYLE]}
OSS_BUCKETNAME = {
    "bucket_name": {"bucket": 'BUCKET', "domain": "DOMAIN",
                    "style": ["style1", "style2"]},
}
