from django.test import TestCase

# Create your tests here.

import os
# 可用于拆分settings.py 为生产换景、开发环境
# 这样就可以通过设定环境变量PROJECT_PROFILE 为develop 或者product ，让Django 加载不同的配置。
profile = os.environ.get('PROJECT_PROFILE', 'develop')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'nlp3_cbv.settings.%s' % profile)
print(profile)
