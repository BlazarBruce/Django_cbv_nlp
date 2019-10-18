from django.urls import path, re_path
from nlp_web import views

# url分发器
urlpatterns = [
    path('', views.hello, name='hello'),
    re_path(r'^query/(.+)/$', views.nlpView.as_view(), name='index'),

]

