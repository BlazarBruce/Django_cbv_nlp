"""
参考链接：https://www.cnblogs.com/wupeiqi/articles/7805382.html
目前实现功能：认证、权限
认证返回：3总情况、返回元祖、返回noen 、抛出异常
权限返回两种情况; True:有权限、False:无权限
"""

from rest_framework.views import APIView  # django rest framework 提供的 APIView
from rest_framework.response import Response  # django rest framework 渲染器
from api.utills.authenticate import TestAuthentication1  # a. 用户url传入的token认证
from api.utills.authenticate import TestAuthentication2  # b. 请求头认证
from api.utills.authenticate import Test1Authentication, Test2Authentication  # 用于多规则认证
from api.utills.permission import TestPermission  # 自定义权限类


class TestView(APIView):
    # 均是对单独视图进行特殊配置，如果想要对全局进行配置，则需要再配置文件中写入即可。
    # 并且删除类中的 authentication_classes = [TestAuthentication1, ] 设置否则全局设置无效
    authentication_classes = [TestAuthentication1, ]  # 认证类
    # authentication_classes = [Test1Authentication, Test2Authentication]  # 多规则认证
    permission_classes = [TestPermission, ]  # 权限类

    def get(self, request, *args, **kwargs):
        # self.dispatch()  # 源码分析入口
        print(request.user)
        print(request.auth)
        return Response('GET请求，响应内容')

    def post(self, request, *args, **kwargs):
        return Response('POST请求，响应内容')

    def put(self, request, *args, **kwargs):
        return Response('PUT请求，响应内容')






