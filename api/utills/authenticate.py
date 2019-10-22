"""
token 认证
"""
from rest_framework.authentication import BaseAuthentication  # 认证类
from rest_framework import exceptions
"""
问题：怎样从封装的数据中取出自己想要的数据
"""

# token列表、该列表已经写入数据库中
token_list = [
    'sfsfss123kuf3j123',
    'asijnfowerkkf9812',
]

# 第一版
# a. 用户url传入的token认证
class TestAuthentication1(BaseAuthentication):
    def authenticate(self, request):
        """
        用户认证，如果验证成功后返回元组： (用户,用户Token)
        :param request:
        :return:
            None,表示跳过该验证；
                如果跳过了所有认证，默认用户和Token和使用配置文件进行设置
                self._authenticator = None
                if api_settings.UNAUTHENTICATED_USER:
                    self.user = api_settings.UNAUTHENTICATED_USER()
                else:
                    self.user = None

                if api_settings.UNAUTHENTICATED_TOKEN:
                    self.auth = api_settings.UNAUTHENTICATED_TOKEN()
                else:
                    self.auth = None
            (user,token)表示验证通过并设置用户名和Token；
            AuthenticationFailed异常
        """
        val = request.query_params.get('token')  # 用户url传入的token认证
        # 如果数据库中没有token、认证失败(此处的token写在程序中）
        if val not in token_list:
            raise exceptions.AuthenticationFailed("用户认证失败")
        # 如果数据库中存在则返回(user,token)
        return ('登录用户', '用户token')

    def authenticate_header(self, request):
        """
        Return a string to be used as the value of the `WWW-Authenticate`
        header in a `401 Unauthenticated` response, or `None` if the
        authentication scheme should return `403 Permission Denied` responses.
        """
        # 验证失败时，返回的响应头WWW-Authenticate对应的值
        pass



# b. 请求头认证
class TestAuthentication2(BaseAuthentication):
    def authenticate(self, request):
        """
        用户认证，如果验证成功后返回元组： (用户,用户Token)
        :param request:
        :return:
            None,表示跳过该验证；
                如果跳过了所有认证，默认用户和Token和使用配置文件进行设置
                self._authenticator = None
                if api_settings.UNAUTHENTICATED_USER:
                    self.user = api_settings.UNAUTHENTICATED_USER()
                else:
                    self.user = None

                if api_settings.UNAUTHENTICATED_TOKEN:
                    self.auth = api_settings.UNAUTHENTICATED_TOKEN()
                else:
                    self.auth = None
            (user,token)表示验证通过并设置用户名和Token；
            AuthenticationFailed异常
        """
        import base64
        auth = request.META.get('HTTP_AUTHORIZATION', b'')
        if auth:
            auth = auth.encode('utf-8')
        auth = auth.split()
        if not auth or auth[0].lower() != b'basic':
            raise exceptions.AuthenticationFailed('验证失败')
        if len(auth) != 2:
            raise exceptions.AuthenticationFailed('验证失败')
        username, part, password = base64.b64decode(auth[1]).decode('utf-8').partition(':')
        if username == 'alex' and password == '123':
            return ('登录用户', '用户token')
        else:
            raise exceptions.AuthenticationFailed('用户名或密码错误')

    def authenticate_header(self, request):
        """
        Return a string to be used as the value of the `WWW-Authenticate`
        header in a `401 Unauthenticated` response, or `None` if the
        authentication scheme should return `403 Permission Denied` responses.
        """
        return 'Basic realm=api'

# c. 多个认证规则
class Test1Authentication(BaseAuthentication):
    def authenticate(self, request):
        """
        用户认证，如果验证成功后返回元组： (用户,用户Token)
        :param request:
        :return:
            None,表示跳过该验证；
                如果跳过了所有认证，默认用户和Token和使用配置文件进行设置
                self._authenticator = None
                if api_settings.UNAUTHENTICATED_USER:
                    self.user = api_settings.UNAUTHENTICATED_USER() # 默认值为：匿名用户
                else:
                    self.user = None

                if api_settings.UNAUTHENTICATED_TOKEN:
                    self.auth = api_settings.UNAUTHENTICATED_TOKEN()# 默认值为：None
                else:
                    self.auth = None
            (user,token)表示验证通过并设置用户名和Token；
            AuthenticationFailed异常
        """
        import base64
        auth = request.META.get('HTTP_AUTHORIZATION', b'')
        if auth:
            auth = auth.encode('utf-8')
        else:
            return None
        print(auth, 'xxxx')
        auth = auth.split()
        if not auth or auth[0].lower() != b'basic':
            raise exceptions.AuthenticationFailed('验证失败')
        if len(auth) != 2:
            raise exceptions.AuthenticationFailed('验证失败')
        username, part, password = base64.b64decode(auth[1]).decode('utf-8').partition(':')
        if username == 'alex' and password == '123':
            return ('登录用户', '用户token')
        else:
            raise exceptions.AuthenticationFailed('用户名或密码错误')

    def authenticate_header(self, request):
        """
        Return a string to be used as the value of the `WWW-Authenticate`
        header in a `401 Unauthenticated` response, or `None` if the
        authentication scheme should return `403 Permission Denied` responses.
        """
        # return 'Basic realm=api'
        pass


class Test2Authentication(BaseAuthentication):
    def authenticate(self, request):
        """
        用户认证，如果验证成功后返回元组： (用户,用户Token)
        :param request:
        :return:
            None,表示跳过该验证；
                如果跳过了所有认证，默认用户和Token和使用配置文件进行设置
                self._authenticator = None
                if api_settings.UNAUTHENTICATED_USER:
                    self.user = api_settings.UNAUTHENTICATED_USER() # 默认值为：匿名用户
                else:
                    self.user = None

                if api_settings.UNAUTHENTICATED_TOKEN:
                    self.auth = api_settings.UNAUTHENTICATED_TOKEN()# 默认值为：None
                else:
                    self.auth = None
            (user,token)表示验证通过并设置用户名和Token；
            AuthenticationFailed异常
        """
        val = request.query_params.get('token')
        if val not in token_list:
            raise exceptions.AuthenticationFailed("用户认证失败")

        return ('登录用户', '用户token')

    def authenticate_header(self, request):
        """
        Return a string to be used as the value of the `WWW-Authenticate`
        header in a `401 Unauthenticated` response, or `None` if the
        authentication scheme should return `403 Permission Denied` responses.
        """
        pass



