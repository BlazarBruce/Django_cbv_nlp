from django.urls import path
from blog_comment import views

# url分发器
urlpatterns = [
    path('temp/', views.myMap.as_view(), name='myMap'),

]
