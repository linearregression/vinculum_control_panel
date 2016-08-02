from django.shortcuts import render

# Create your views here.
from rest_framework import generics
from rest_framework import permissions


from vinculum.models import Vinculum
from vinculum.serializers import VinculumSerializer


class VinculumList(generics.ListCreateAPIView):
    queryset = Vinculum.objects.all()
    serializer_class = VinculumSerializer
    # handles get, post

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    # permission_classes = (permissions.IsAuthenticated,)
    #

class VinculumDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Vinculum.objects.all()
    serializer_class = VinculumSerializer

    # permission_classes = (permissions.IsAuthenticated,)

    #handles get, put, delete
