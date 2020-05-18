#!/usr/bin/python
# -*- coding:utf-8 -*-
# 阿里云oss操作
import oss2
from .config import *
from hashlib import md5
from os import path
import requests


class OssManager:

    def __init__(self):
        self.key_id = OSS_ACCESS_KEY_ID
        self.key_secret = OSS_ACCESS_KEY_SECRET
        self.end_point = OSS_END_POINT

    # 根据用途获取bucket
    def get_bucket(self, type='cover'):
        if type == 'cover':
            return OSS_BUCKETNAME[0]
        else:
            return OSS_BUCKETNAME[1]

    def get_domain(self, bucket):
        return OSS_DOMAIN[bucket]

    def upload(self, bucket_name, src, shelf_id):
        if bucket_name not in OSS_BUCKETNAME:
            raise OssException("不存在的bucket")

        auth = oss2.Auth(self.key_id, self.key_secret)
        bucket = oss2.Bucket(auth, self.end_point, bucket_name)

        # 格式：/shelf_id/md5(不带扩展名的src路径)[0:8].扩展名
        fname, extname = path.splitext(src)
        if len(extname) > 0:
            extname = "." + extname

        m = md5()
        m.update(fname.encode(encoding='utf-8'))
        str_md5 = m.hexdigest()
        dest = "%s/%s%s" % (shelf_id, str_md5[0:8], extname)

        # 网络流上传
        input = requests.get(src)
        bucket.put_object(dest, input)
        print("%s/%s" % (self.get_domain(bucket_name), dest))
        return dest

    def get_url(self, key, bucket_name):
        return "//%s/%s" % (self.get_domain(bucket_name), key)


class OssException(Exception):
    pass
