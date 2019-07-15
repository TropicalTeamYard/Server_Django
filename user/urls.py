from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('create', views.create, name='create'),
    path('check_name', views.check_name, name='check_name'),
    path('login', views.login, name='login'),
]
