from __future__ import unicode_literals

from django.contrib.auth.models import User
from django.db import models

from separatedvaluesfield.models import  SeparatedValuesField

# Create your models here.


class Vinculum(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=100, blank=True, default='')
    owner = models.ForeignKey(User, related_name='vinculum')
    root_path = models.CharField(max_length=1024, blank=True)

    class Meta:
        ordering = ('created',)

    # def create(self, validated_data):
    #     # remoteresources = validated_data.pop('remoteresources')
    #     # inputpaths =
    #     pass


class RemoteResources(models.Model):
    vinculum = models.ForeignKey(Vinculum, on_delete=models.CASCADE, related_name="remote_resources")
    # make sure to set related_name to this so it maches what is in the VinculumSerializer's Meta 'fields' member

    authentication_behavior = models.CharField(max_length=100, blank=True, default='')
    # how do we authenticate against this remote resource?

    remote_resource_path = models.TextField(blank=False)
    # where do we find this remote resource? Expect something like an API

    def __unicode__(self):
        return '%s : %s' % (self.remote_resource_path, self.output_path)


class InputOutputPath(models.Model):
    remote_resource = models.ForeignKey(RemoteResources, on_delete=models.CASCADE, related_name="io_paths")
    input_path = models.TextField()
    output_path = models.TextField()

    def __unicode__(self):
        return '%s : %s' % (self.input_path, self.output_path)