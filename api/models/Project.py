from django.db import models


class Project(models.Model):
    name = models.CharField(max_length=200)
    path = models.CharField(max_length=200, default='')
    created_at = models.DateTimeField(auto_now_add=True)