from django.shortcuts import render
from django.views import View

# 多媒体访问
# 访问url http://127.0.0.1:8000/media/video/
class myMedia(View):

    def get(self, request, *args, **kwargs):
        return render(request, 'video.html')

