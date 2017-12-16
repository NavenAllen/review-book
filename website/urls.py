from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('auth', views.auth, name='auth'),
    path('register', views.register, name='register'),
    path('home', views.home, name='home'),
    path('search', views.search, name='search')
]