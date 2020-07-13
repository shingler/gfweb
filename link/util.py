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
    def get_bucket(self, bucket_name='cover'):
        if bucket_name in OSS_BUCKETNAME:
            return OSS_BUCKETNAME[bucket_name]["bucket"]
        else:
            return ""

    def get_domain(self, bucket_name):
        # print(bucket_name)
        if bucket_name in OSS_BUCKETNAME:
            return OSS_BUCKETNAME[bucket_name]["domain"]
        else:
            return ""

    def get_style(self, bucket_name):
        if bucket_name in OSS_BUCKETNAME:
            return OSS_BUCKETNAME[bucket_name]["style"]
        else:
            return ""

    # 由id和src生成远端代码名
    def get_remote_key(self, shelf_id, src):
        # 格式：/shelf_id/md5(不带扩展名的src路径)[0:8].扩展名
        fname, extname = path.splitext(src)

        m = md5()
        m.update(fname.encode(encoding='utf-8'))
        str_md5 = m.hexdigest()
        dest = "%s/%s%s" % (shelf_id, str_md5[0:8], extname)
        return dest

    # 指定key是否已存在
    def is_exist(self, bucket_name, key):
        bucket = self.get_bucket(bucket_name)
        if bucket == "":
            raise OssException("不存在的bucket")
        auth = oss2.Auth(self.key_id, self.key_secret)
        bucket = oss2.Bucket(auth, self.end_point, bucket)
        return bucket.object_exists(key)


    # 上传
    def upload(self, bucket_name, src, shelf_id):
        bucket = self.get_bucket(bucket_name)
        if bucket == "":
            raise OssException("不存在的bucket")

        auth = oss2.Auth(self.key_id, self.key_secret)
        bucket = oss2.Bucket(auth, self.end_point, bucket)

        dest = self.get_remote_key(shelf_id, src)
        # 实体是否已创建
        if self.is_exist(bucket_name, dest):
            print("%s已存在" % dest)
            return dest

        # 网络流上传
        input = requests.get(src)
        bucket.put_object(dest, input)
        print("%s/%s" % (self.get_domain(bucket_name), dest))
        return dest

    # 获取缩略图地址
    def get_url(self, key, bucket_name, style_name=""):
        origin_url = self.get_origin_url(key, bucket_name)
        if style_name in self.get_style(bucket_name):
            return "%s?x-oss-process=style/%s" % (origin_url, style_name)
        else:
            return origin_url

    # 获取原图地址
    def get_origin_url(self, key, bucket_name):
        return "//%s/%s" % (self.get_domain(bucket_name), key)


class OssException(Exception):
    pass
