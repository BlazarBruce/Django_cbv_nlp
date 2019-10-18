from django.urls import path
from my_media import views

# url分发器
urlpatterns = [
    path('video/', views.myMedia.as_view(), name='myVideo'),

]