# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.
class User(models.Model):
    _id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=30)
    password = models.CharField(max_length=30)

    class Meta:
        db_table = 'users'

class Review(models.Model):
    _id = models.AutoField(primary_key=True)
    review_for = models.ForeignKey(User, on_delete=models.CASCADE, related_name="assignee")
    review_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="creator")
    upvotes = models.IntegerField(default=0)
    downvotes = models.IntegerField(default=0)
    title = models.CharField(max_length=15)
    text = models.CharField(max_length=240)

    class Meta:
        db_table = 'reviews'




        