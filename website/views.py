# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.template import loader
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse

from .models import User


# Create your views here.
def index(request):
    if(request.session.get('user')):
        return render(request, 'website/home.html')
    else:
        return render(request, 'website/index.html')

def auth(request):
    try:
        selected_user = User.objects.get(user_name=request.POST['user_name'], password=request.POST['password'])
        request.session['user'] = selected_user.user_name;
    except (KeyError, User.DoesNotExist):
        return render(request, 'website/index.html', {
            'error_message': "Invalid Credentials.",
        })
    else:
        return HttpResponseRedirect(reverse('home'))

def register(request):
     newUser = User(user_name=request.POST['user_name'], password=request.POST['password'])
     newUser.save()
     return HttpResponseRedirect(reverse('index'))

def home(request):
    return render(request, 'website/home.html')

def search(request):
    searched_user = User.objects.get(user_name=request.GET['search_query'])
    template = loader.get_template('polls/profile.html')
    context = {
        'user': searched_user,
    }
    return HttpResponse(template.render(context, request))

