#!/usr/bin/python
# -*- coding:utf-8 -*-
# 处理第三方登录逻辑
import json
import logging

import ssl
import time

from django.contrib.auth import login, logout
from django.contrib.auth.models import User
from django.shortcuts import render

from authApp.models import Connect, UserProfile

from alipay.aop.api.request.AlipaySystemOauthTokenRequest import AlipaySystemOauthTokenRequest
from alipay.aop.api.request.AlipayUserInfoShareRequest import AlipayUserInfoShareRequest
from alipay.aop.api.response.AlipaySystemOauthTokenResponse import AlipaySystemOauthTokenResponse
from alipay.aop.api.response.AlipayUserInfoShareResponse import AlipayUserInfoShareResponse
from django.conf import settings
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseBadRequest
from authApp import config
from alipay.aop.api.AlipayClientConfig import AlipayClientConfig
from alipay.aop.api.DefaultAlipayClient import DefaultAlipayClient


class connect:
    # 跳转到授权页地址
    def authorize(request):
        pass

    # oauth登录流程
    def token(request):
        pass

    # 退出登录
    def logout(request):
        ref = request.GET.get("ref") if request.GET.get("ref") is not None else "/"
        logout(request)
        return HttpResponseRedirect(ref)


# 支付宝登录逻辑
class alipay(connect):

    # 授权页地址
    def authorize(request):
        ref = request.GET["ref"] if request.GET["ref"] is not None else "/"
        alipay_config = config.Alipay(is_sandbox=False)
        url = alipay_config.GATEWAY % (alipay_config.APP_ID, alipay_config.REDIRECT_URI + "?ref=" + ref)
        # return HttpResponse(url)
        return HttpResponseRedirect(url)

    # oauth登录流程
    def token(request):
        ref = request.GET.get("ref") if request.GET.get("ref") is not None else "/"
        if ref == request.path:
            ref = "/"

        # 没有auth_code未登录，算错误的请求
        if request.GET.get("auth_code") is None and not request.user.is_authenticated:
            return render(request, "weui/siginin/fail.html", {"msg": "错误的请求", "ref": ref})

        # 没有auth_code已登录，跳转ref
        if request.GET.get("auth_code") is None and request.user.is_authenticated:
            return render(request, "weui/siginin/success.html", {"ref": ref})

        # 有auth_code未登录，走登录流程
        if request.GET.get("auth_code") is not None:
            auth_code = request.GET["auth_code"]
            ssl._create_default_https_context = ssl._create_unverified_context
            # 通过auth_code获取access_token及用户信息
            alipay_config = config.Alipay(is_sandbox=True if settings.CONNECT_ALIPAY == "sandbox" else False)

            logging.basicConfig(
                level=logging.INFO,
                format='%(asctime)s %(levelname)s %(message)s',
                filemode='a', )
            logger = logging.getLogger('')

            alipay_client_config = AlipayClientConfig(sandbox_debug=False)
            alipay_client_config.server_url = 'https://openapi.alipay.com/gateway.do'
            alipay_client_config.app_id = alipay_config.APP_ID
            alipay_client_config.app_private_key = alipay_config.PRIVATE_KEY
            alipay_client_config.alipay_public_key = alipay_config.ALIPAY_PUBLIC_KEY

            alipayClient = DefaultAlipayClient(alipay_client_config=alipay_client_config, logger=logger)
            # 获取token
            tokenRequest = AlipaySystemOauthTokenRequest()
            tokenRequest.code = auth_code
            tokenRequest.grant_type = "authorization_code"
            response_content = ""
            access_token = {}
            try:
                response_content = alipayClient.execute(tokenRequest)
            except Exception as ex:
                print(ex)

            if not response_content:
                return render(request, "weui/siginin/fail.html", {"msg": "错误的请求", "ref": ref})

            oauthTokenResponse = AlipaySystemOauthTokenResponse()
            oauthTokenResponse.parse_response_content(response_content)
            if not oauthTokenResponse.is_success():
                return render(request, "weui/siginin/fail.html", {"msg": oauthTokenResponse.sub_msg, "ref": ref})

            # 判断用户是否存在
            platform_user_id = oauthTokenResponse.user_id
            connectObj = Connect.objects.filter(oauth_platform_user_id=platform_user_id).first()
            if connectObj is not None:
                # 可以登录
                user = User.objects.get(id=connectObj.user_id)
                login(request, user)
                return render(request, "weui/siginin/success.html", {"ref": ref})

            # 构建模型，取得用户信息后即可注册
            connectObj = Connect()
            connectObj.oauth_expire = time.time() + oauthTokenResponse.expires_in
            connectObj.oauth_key = alipay_client_config.app_id
            connectObj.oauth_platform = "alipay"
            connectObj.oauth_platform_user_id = platform_user_id
            connectObj.oauth_token = oauthTokenResponse.access_token
            connectObj.oauth_token_fresh = oauthTokenResponse.refresh_token
            connectObj.oauth_token_fresh_expire = time.time() + oauthTokenResponse.re_expires_in
            connectObj.created = time.time()

            print(oauthTokenResponse.access_token)

            # 获取用户信息
            user_info_request = AlipayUserInfoShareRequest()
            user_info_request.udf_params = {"auth_token": oauthTokenResponse.access_token}
            response_content = alipayClient.execute(user_info_request)
            infoResponse = AlipayUserInfoShareResponse()
            infoResponse.parse_response_content(response_content)
            print(infoResponse)
            print(infoResponse.user_id, infoResponse.nick_name)
            # 保存新用户信息
            user = User.objects.create_user(username=infoResponse.nick_name)
            user.save()
            user_profile = UserProfile()
            user_profile.user_id = user.id
            user_profile.nickname = infoResponse.nick_name
            user_profile.avatar = infoResponse.avatar
            user_profile.save()
            connectObj.user_id = user.id
            connectObj.oauth_data = response_content
            connectObj.save()

            return HttpResponse(connectObj.user_id)


class wx(connect):
    pass

