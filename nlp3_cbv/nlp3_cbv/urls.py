"""nlp3_cbv URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin  # 默认进入django页面
from django.urls import path, include
from nlp_web import views


urlpatterns = [
    path('', views.hello, name='hello'),                 # 首页界面
    path('admin/', admin.site.urls),                     # 后台管理模块
    path('nlp/', include('nlp_web.urls')),                  # 第一个app包含的所有url(自然语言处理）
    path('blogs/', include('blog_comment.urls')),           # 第二个app包含的所有url(博客系统）
    path('media/', include('my_media.urls')),               # 第三个app包含的所有url(多媒体系统）
    path('location/', include('location_transform.urls')),  # 第四个app包含的所有url(经纬度转换系统）
    path('api/', include('api.urls')),  # 第四个app包含的所有url(经纬度转换系统）
    path('student/', include('student_sys.urls')),  # 第四个app包含的所有url(学生系统）
]

