from django.conf.urls import url, include
from django.contrib import admin
from student_sys.views import index, IndexView

urlpatterns = [
    # url(r'^$', index, name='index'),  # 欢迎界面的url\ name='index' 用于找到对应的url、从而完成重定向
    url(r'^$', IndexView.as_view(), name='index'),  # 基于CBV的实现
    url(r'^admin/', admin.site.urls),

]
