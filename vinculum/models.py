from __future__ import unicode_literals

from django.contrib.auth.models import User
from django.db import models

from separatedvaluesfield.models import  SeparatedValuesField

# Create your models here.

class Vinculum(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=100, blank=True, default='')
    input_paths = SeparatedValuesField(max_length=1024)
    output_path = models.TextField()
    remote_resource = models.TextField(blank=False)

    authentication = models.CharField(max_length=100, blank=True, default='')

    owner = models.ForeignKey(User, related_name='vinculum')

    class Meta:
        ordering = ('created',)

    def save(self, *args, **kwargs):
        super(Vinculum, self).save(*args, **kwargs)
