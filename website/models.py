# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.
class User(models.Model):
    user_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=30)
    password = models.CharField(max_length=30)

    class Meta:
        db_table = 'users'

   
class Review(models.Model):
    review_id = models.AutoField(primary_key=True)
    review_for = models.ForeignKey(User, on_delete=models.CASCADE, related_name="assignee")
    review_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="creator")
    upvotes = models.IntegerField(default=0)
    downvotes = models.IntegerField(default=0)
    title = models.CharField(max_length=30)
    text = models.CharField(max_length=240)
    published = models.BooleanField(default=False)

    class Meta:
        db_table = 'reviews'


class GroupMembers(models.Model):
    group_member_id = models.AutoField(primary_key=True)
    group_id = models.IntegerField(default=0)
    name = models.CharField(max_length=30)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="group_members")
    
    class Meta:
        db_table = 'group_members'

class GroupReview(models.Model):
    group_review_id = models.AutoField(primary_key=True)
    agreed = models.IntegerField(default=0)
    disagreed = models.IntegerField(default=0)
    group_id = models.IntegerField()
    review = models.ForeignKey(Review, on_delete=models.CASCADE)
    agreed_percent = models.FloatField(default=0)

    class Meta:
        db_table = 'group_reviews'

    
    




        
