from django.db import models
from .Project import Project


class Collection(models.Model):
    name = models.CharField(max_length=200)
    path = models.CharField(max_length=200, default='')
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)