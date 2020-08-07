#!/usr/bin/python
# -*- coding:utf-8 -*-


class AuthConfig:

    @property
    def APP_ID(self):
        return self._sandbox["APP_ID"] if self.is_sandbox else self._production["APP_ID"]

    @property
    def REDIRECT_URI(self):
        return self._sandbox["REDIRECT_URI"] if self.is_sandbox else self._production["REDIRECT_URI"]

    @property
    def GATEWAY(self):
        return self._sandbox["GATEWAY"] if self.is_sandbox else self._production["GATEWAY"]

    @property
    def PRIVATE_KEY(self):
        return self._sandbox["PRIVATE_KEY"] if self.is_sandbox else self._production["PRIVATE_KEY"]

    @property
    def PUBLIC_KEY(self):
        return self._sandbox["PUBLIC_KEY"] if self.is_sandbox else self._production["PUBLIC_KEY"]

    @property
    def ALIPAY_PUBLIC_KEY(self):
        return self._sandbox["ALIPAY_PUBLIC_KEY"] if self.is_sandbox else self._production["ALIPAY_PUBLIC_KEY"]


# 支付宝登录配置
class Alipay(AuthConfig):

    def __init__(self, is_sandbox=False):
        self.is_sandbox = is_sandbox
        self._sandbox = {
            "APP_ID": "",
            "REDIRECT_URI": "",
            "GATEWAY": "",
            "PRIVATE_KEY": "",
            "PUBLIC_KEY": "",
            "ALIPAY_PUBLIC_KEY": "",
        }
        self._production = {
            "APP_ID": "",
            "REDIRECT_URI": "",
            "GATEWAY": "",
            "PRIVATE_KEY": "",
            "PUBLIC_KEY": "",
            "ALIPAY_PUBLIC_KEY": "",
        }


# 微信登录配置
class Wx(AuthConfig):
    def __init__(self, is_sandbox=False):
        self.is_sandbox = is_sandbox
        self._sandbox = {
            "APP_ID": "",
            "REDIRECT_URI": "",
            "GATEWAY": "",
            "PRIVATE_KEY": "",
            "PUBLIC_KEY": "",
            "ALIPAY_PUBLIC_KEY": "",
        }
        self._production = {
            "APP_ID": "",
            "REDIRECT_URI": "",
            "GATEWAY": "",
            "PRIVATE_KEY": "",
            "PUBLIC_KEY": "",
            "ALIPAY_PUBLIC_KEY": "",
        }