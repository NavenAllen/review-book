# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.template import loader
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse

from .models import User, Review


# Create your views here.
def index(request):
    if(request.session.get('user_logged_id')):
        return render(request, 'website/home.html')
    else:
        return render(request, 'website/index.html')

def auth(request):
    try:
        selected_user = User.objects.get(name=request.POST['user_name'], password=request.POST['password'])
        request.session['user_logged_name'] = selected_user.name
        request.session['user_logged_id'] = selected_user._id
    except (KeyError, User.DoesNotExist):
        return render(request, 'website/index.html', {
            'error_message': "Invalid Credentials.",
        })
    else:
        return HttpResponseRedirect(reverse('home'))

def register(request):
     newUser = User(name=request.POST['user_name'], password=request.POST['password'])
     newUser.save()
     return HttpResponseRedirect(reverse('index'))

def home(request):
    return render(request, 'website/home.html')

def search(request):
    try:
            searched_user = User.objects.get(name=request.GET['search_query'])
    except (KeyError, User.DoesNotExist):
        return render(request, 'website/home.html', {
            'error_message': "Not able to find user.",
        })
    else:
        request.session['user_visited_id'] = searched_user._id
        return HttpResponseRedirect(reverse('profile'))

def create_review(request):
    new_review = Review(text=request.POST['review_text'], title=request.POST['review_title'])
    new_review.save()
    return HttpResponseRedirect(reverse('profile'))

def profile(request):
    user_visited_id = request.session['user_visited_id']
    user_visited = User.objects.get(pk=user_visited_id)
    user_reviews = Review.objects.filter(review_for=user_visited._id)
    print (user_reviews)
    template = loader.get_template('website/profile.html')
    context = {
            'user': user_visited,
            'user_reviews': user_reviews
    }
    return HttpResponse(template.render(context, request))

def logout(request):
    for key in request.session.keys():
        del request.session[key]
    return HttpResponseRedirect(reverse('index'))





