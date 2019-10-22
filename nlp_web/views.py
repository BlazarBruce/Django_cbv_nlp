from rest_framework.views import APIView
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer  # 渲染器
from rest_framework import serializers  # 序列化

from nlp_web.model_parts import model_manage  # domain分发主逻辑

# 初始展示界面
def hello(request):
    return render(request, 'welcome.html')

# 目前仅仅处理get请求
class nlpView(APIView):
    # renderer_classes = [JSONRenderer, ]  # 注册渲染器类、以json的方式返回
    def get(self, request, *args, **kwargs):
        result = model_manage.domain_distribute(*args)  # 获取url中的参数
        return Response(result)  # 进行数据渲染

    def post(self, request, *args, **kwargs):
        result = {
            'status': True,
            'data': 'response data'
        }
        return Response(result)

    def delete(self, request, *args, **kwargs):
        result = {
            'status': True,
            'data': 'response data'
        }
        return Response(result)

    def put(self, request, *args, **kwargs):
        result = {
            'status': True,
            'data': 'response data'
        }
        return Response(result)

    def patch(self, request, *args, **kwargs):
        result = {
            'status': True,
            'data': 'response data'
        }
        return Response(result)

    def options(self, request, *args, **kwargs):
        result = {
            'status': True,
            'data': 'response data'
        }
        return Response(result)



