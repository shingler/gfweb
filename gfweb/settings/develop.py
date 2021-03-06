#!/usr/bin/python
# -*- coding:utf-8 -*-
"""
Django settings for gfweb project.

Generated by 'django-admin startproject' using Django 2.0.4.

For more information on this file, see
https://docs.djangoproject.com/en/2.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.0/ref/settings/
"""
import os
from .base import *

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '*74sufjll3c(oc(=_9#0uy(%nb-o651f@ct0g1s4m2ab*v@@f)'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ["*"]

# Database
# https://docs.djangoproject.com/en/2.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'game_finder',
        'USER': 'root',
        'PASSWORD': '123456',
        'HOST': '127.0.0.1',
        # 'HOST': '172.17.0.2',
        'PORT': '3306'
    }
}

CONNECT_ALIPAY = "production"
