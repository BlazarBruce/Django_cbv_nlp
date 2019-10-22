"""
目的：造一个middleware逐渐、用来练习
功能：统计首页每次访问程序所消耗的时间

"""
import time
from django.urls import reverse
from django.utils.deprecation import MiddlewareMixin  # Django提供的中间键类

class TimeItMiddleware(MiddlewareMixin):
    def process_request(self, request):
        self.start_time = time.time()
        return

    def process_view(self, request, func, *args, **kwargs):
        if request.path != reverse('index'):
            return None
        start = time.time()
        response = func(request)
        costed = time.time() - start
        print('process_view {:.2f}s'.format(costed))
        return response

    def process_exception(self, request):
        pass

    def process_template_response(self, request, response):
        return response

    def process_response(self, request, response):
        costed = time.time() - self.start_time
        print('request to response cost {:.2f}s'.format(costed))
        return response
