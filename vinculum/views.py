import json

from django.shortcuts import render

# Create your views here.
from rest_framework import generics
from rest_framework import permissions

import requests

from control_panel.settings import VINCULUM_RUNNER
from vinculum.models import Vinculum
from vinculum.serializers import VinculumSerializer
from rest_framework.renderers import JSONRenderer


class VinculumList(generics.ListCreateAPIView):
    # queryset = Vinculum.objects.all()
    serializer_class = VinculumSerializer
    # handles get, post

    def get_queryset(self):
            return Vinculum.objects.filter(owner=self.request.user)

    def perform_create(self, serializer):
        instance = serializer.save(owner=self.request.user)

        vinculum_serialized_data = JSONRenderer().render(serializer.validated_data)
        data = {
            'remote_id':instance.id,
            'jobs_json': vinculum_serialized_data
            }
        r = requests.post(VINCULUM_RUNNER, json=data)

    permission_classes = (permissions.IsAuthenticated,)
    #


class VinculumDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Vinculum.objects.all()
    serializer_class = VinculumSerializer

    permission_classes = (permissions.IsAuthenticated,)

    # handles get, put, delete
