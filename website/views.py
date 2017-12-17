# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.template import loader
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse

from .models import User, Review, GroupReview, GroupMembers


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
        request.session['user_logged_id'] = selected_user.user_id
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
    user_logged_id = request.session['user_logged_id']
    user_logged = User.objects.get(pk=user_logged_id)
    group_list = GroupMembers.objects.filter(user=request.session['user_logged_id'])
    template = loader.get_template('website/home.html')
    context = {
            'group_list': group_list,
            'user':user_logged
    }
    return HttpResponse(template.render(context, request))

def search(request):
    try:
            searched_user = User.objects.get(name=request.GET['search_query'])
    except (KeyError, User.DoesNotExist):
        return render(request, 'website/home.html', {
            'error_message': "Not able to find user.",
        })
    else:
        request.session['user_visited_id'] = searched_user.user_id
        return HttpResponseRedirect(reverse('profile'))

def create_review(request):
    user_visited_id = request.session['user_visited_id']
    user_visited = User.objects.get(pk=user_visited_id)
    user_logged_id = request.session['user_logged_id']
    user_logged = User.objects.get(pk=user_logged_id)
    new_review = Review(text=request.POST['review_text'], title=request.POST['review_title'], review_for=user_visited, review_by=user_logged, published=True)
    new_review.save()
    return HttpResponseRedirect(reverse('profile'))

def profile(request):
    user_visited_id = request.session['user_visited_id']
    user_visited = User.objects.get(pk=user_visited_id)
    user_reviews = Review.objects.filter(review_for=user_visited.user_id, published=True)
    template = loader.get_template('website/profile.html')
    context = {
            'user': user_visited,
            'user_reviews': user_reviews
    }
    return HttpResponse(template.render(context, request))

def logout(request):
    for key in list(request.session.keys()):
        del request.session[key]
    return HttpResponseRedirect(reverse('index'))

def createGroup(request):
    max_group = GroupMembers.objects.order_by('-group_id').first()
    user_logged_id = request.session['user_logged_id']
    user_logged = User.objects.get(pk=user_logged_id)
    if(max_group):
        max_group_id = max_group.group_id
    else:
        max_group_id = 0
    new_group = GroupMembers(name=request.POST['group_name'], group_id=max_group_id+1, user=user_logged)
    new_group.save()
    return HttpResponseRedirect(reverse('group', args=(max_group_id+1,)))

def group(request, group_id):
    members_list = GroupMembers.objects.filter(group_id=group_id)
    review_list = GroupReview.objects.filter(group_id=group_id)
    print (review_list)
    group = GroupMembers.objects.filter(group_id=group_id).first()
    template = loader.get_template('website/group.html')
    context = {
            'members_list': members_list,
            'review_list':review_list,
            'group_id': group_id,
            'group':group
    }
    return HttpResponse(template.render(context, request))

def createGroupReview(request, group_id):
    user_logged_id = request.session['user_logged_id']
    user_logged = User.objects.get(pk=user_logged_id)
    user_visited_name = request.POST['review_for']
    user_visited = User.objects.get(name=user_visited_name)
    new_review = Review(text=request.POST['review_text'], title=request.POST['review_title'], review_for=user_visited, review_by=user_logged)
    new_review.save()
    new_group_review = GroupReview(group_id=group_id, review = new_review)
    new_group_review.save()
    return HttpResponseRedirect(reverse('group', args=(group_id,)))

def incrementAgreed(request, review_id, group_id):
    group_review = GroupReview.objects.get(group_review_id=review_id)
    group_count = GroupMembers.objects.filter(group_id=group_id).count()
    group_review.agreed +=1
    group_review.agreed_percent = (group_review.agreed/group_count)*100
    print (group_review.agreed_percent)
    if group_review.agreed_percent > 50:
        group_review.review.published = True
    group_review.review.save()
    group_review.save()
    return HttpResponseRedirect(reverse('group', args=(group_id,)))

def incrementDisagreed(request, review_id, group_id):
    group_review = GroupReview.objects.get(group_review_id=review_id)
    group_count = GroupMembers.objects.filter(group_id=group_id).count()
    group_review.disagreed +=1
    group_review.save()
    return HttpResponseRedirect(reverse('group', args=(group_id,)))

def joinGroup(request, user_id, group_id):
    user = User.objects.get(pk=user_id)
    group = GroupMembers.objects.filter(group_id=group_id).first()
    new_group_member = GroupMembers(name=group.name, group_id=group_id, user=user)
    new_group_member.save()
    return HttpResponseRedirect(reverse('group', args=(group_id,)))












    








