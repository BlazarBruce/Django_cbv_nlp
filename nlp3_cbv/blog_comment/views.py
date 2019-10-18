from django.shortcuts import render
from django.views import View

class myMap(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'hot_map.html')
