from django.conf.urls import url, include
from api.views import TestView

urlpatterns = [
    url(r'^test/', TestView.as_view()),

]

