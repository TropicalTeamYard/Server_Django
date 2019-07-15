from django.shortcuts import render
from django.http import HttpRequest, HttpResponse, Http404
from .models import Page
import time


# Create your views here.
def index(request: HttpRequest):
    title = "404"
    content = "page not found"
    try:
        name = request.GET['name']
        query_set = Page.objects.filter(name=name)
        if query_set.count() > 0:
            query_first = query_set.first()
            title = query_first.title
            content = query_first.content
        else:
            pass
    except KeyError:
        query_set = Page.objects.filter(name='index')
        if query_set.count() > 0:
            query_first = query_set.first()
            title = query_first.title
            content = query_first.content
    return render(request, 'doc/index.html', context={'page': {'title': title}, 'content': content})

