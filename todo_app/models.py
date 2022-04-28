from django.db import models
from django import forms
from django.contrib.auth.models import User


class ToDoList(models.Model):
    name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True)
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    status = models.CharField(max_length=100)