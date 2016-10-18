import json

from django.shortcuts import render

# Create your views here.
from rest_framework import generics
from rest_framework import permissions

from rest_framework.views import APIView

import requests
from rest_framework.exceptions import ValidationError

from control_panel.settings import VINCULUM_RUNNER
from vinculum.models import Vinculum
from vinculum.serializers import VinculumSerializer
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response


class VinculumList(generics.ListCreateAPIView):
    # TODO: What if remote vinculum runner is not running?
    serializer_class = VinculumSerializer

    def get_queryset(self):
            return Vinculum.objects.filter(owner=self.request.user)

    def perform_create(self, serializer):
        instance = serializer.save(owner=self.request.user)

        if serializer.is_valid() is False:
            return ValidationError('Unable to serialize data')

        # TODO: Move this block to a start_vinculum_runner() function
        vinculum_serialized_data = JSONRenderer().render(serializer.data)
        # get .data instead of validated_data because validated_Data leaves out iopaths for some reason
        # TODO: Find out why iopaths doesn't get validated or serialized.
        data = {
            'remote_id':instance.id,
            'jobs_json': vinculum_serialized_data
            }
        r = requests.post(VINCULUM_RUNNER, json=data)

        remote_task_id = r.json().get('id', None)
        if remote_task_id:
            instance.task_id = r.json()['id']
            instance.save()
        else:
            raise ValidationError('Cannot create a vinculum task runner')

    permission_classes = (permissions.IsAuthenticated,)


class VinculumDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Vinculum.objects.all()
    serializer_class = VinculumSerializer

    permission_classes = (permissions.IsAuthenticated,)

    # handles get, put, delete


class VinculumDetailRunning(APIView):

    # permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        pk = kwargs.get('pk', None)
        if pk is None:
            return Response({'error': 'need a vinculum pk number'})

        vinculum = Vinculum.objects.get(pk=pk)

        if vinculum is None:
            return Response({'error': 'cannot locate vinculum with id: %s' % pk})

        url = VINCULUM_RUNNER + str(vinculum.task_id)

        r = requests.get(url)
        if r.status_code != 200:
            return Response({'error': 'Cannot locate remote vinculum running service'})

        is_running = r.json()['running']
        return Response({'running': is_running, 'pk':pk})

    def put(self, request, *args, **kwargs):
        pk = kwargs.get('pk', None)
        if pk is None:
            return Response({})

        vinculum = Vinculum.objects.get(pk=pk)

        url = VINCULUM_RUNNER + str(vinculum.task_id)

        running_status = request.data.get('running', None)
        if running_status is None:
            return Response({'error': "need to specifiy a boolean 'running' variable"})

        if vinculum is None:
            return Response({})

        r = requests.patch(url, {'running' : running_status} )
        if r.status_code != 200:
            return Response({'error': "Running status failed"})

        return Response({'status': "succeeded"})
