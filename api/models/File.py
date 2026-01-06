from django.db import models
from .Collection import Collection


class File(models.Model):
    name = models.CharField(max_length=200)
    path = models.CharField(max_length=200)
    size = models.IntegerField(default=0)
    collection = models.ForeignKey(Collection, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)