from django.db import models


class Device(models.Model):
    name = models.CharField(max_length=200)
    ip = models.CharField(max_length=15)
    device_id = models.CharField(max_length=5)
    cameras = models.JSONField(default={})
    statistics = models.JSONField(default={})
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)