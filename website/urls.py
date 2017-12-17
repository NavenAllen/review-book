from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('auth', views.auth, name='auth'),
    path('register', views.register, name='register'),
    path('home', views.home, name='home'),
    path('search', views.search, name='search'),
    path('createReview', views.create_review, name='createReview'),
    path('profile', views.profile, name='profile'),
    path('logout', views.logout, name='logout'),
    path('createGroup', views.createGroup, name='createGroup'),
    path(r'^(?P<group_id>[0-9]+)/group', views.group, name='group'),
    path(r'^(?P<group_id>[0-9]+)/createGroupReview', views.createGroupReview, name='createGroupReview'),
    path(r'^(?P<review_id>[0-9]+)/(?P<group_id>[0-9]+)/incrementAgreed$', views.incrementAgreed, name='incrementAgreed'),
    path(r'^(?P<review_id>[0-9]+)/(?P<group_id>[0-9]+)/incrementDisagreed$', views.incrementDisagreed, name='incrementDisagreed'),
    path(r'^(?P<user_id>[0-9]+)/(?P<group_id>[0-9]+)/joinGroup$', views.joinGroup, name='joinGroup') 
]