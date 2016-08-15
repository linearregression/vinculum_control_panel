from django.contrib.auth.models import User
import json

from .models import Vinculum, RemoteResources, InputOutputPath
from rest_framework.test import APITestCase
from rest_framework import status

from serializers import VinculumSerializer


class VinculumSerializeTest(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user('testuser', email='testuser@test.com', password='testing')
        self.user.save()
        self.data = """{
            "title": "Actual real data",
            "root_path": "/mjk4",
            "remote_resources": [{
                "authentication_behavior": "none",
                "remote_resource_path": "https://query.yahooapis.com/v1/public/yql?q=select%20*%20from%20weather.forecast%20where%20woeid%20in%20(select%20woeid%20from%20geo.places(1)%20where%20text%3D%22nome%2C%20ak%22)&format=json&env=store%3A%2F%2Fdatatables.org%2Falltableswithkeys",
                "io_paths": [{
                    "input_path": "query.results.channel",
                    "output_path": "yahoo.weather"
                }]
            }]
        }"""
        self.data_json = json.loads(self.data)
        self.remote_resource_path = "https://query.yahooapis.com/v1/public/yql?q=select%20*%20from%20weather.forecast%20where%20woeid%20in%20(select%20woeid%20from%20geo.places(1)%20where%20text%3D%22nome%2C%20ak%22)&format=json&env=store%3A%2F%2Fdatatables.org%2Falltableswithkeys"

    def _require_login(self):
        self.client.login(username='testuser', password='testing')

    def _login_post_vinculum(self):

        self._require_login()

        response = self.client.post('/vinculums/', json.loads(self.data), format='json')

        return response

    def test_was_vinclum_correctly_serialized(self):

        response = self._login_post_vinculum()

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        vinculum = Vinculum.objects.get(pk=1)
        self.assertTrue(isinstance(vinculum, Vinculum))

        serialized_vinculum = VinculumSerializer(vinculum)

        # self.assertTrue(serialized_vinculum.is_valid())
        # serialized_vinculum_data = serialized_vinculum.validated_data
        # TODO: Find out why this validated_data is different from just plain old 'data' member

        serialized_vinculum_data = serialized_vinculum.data

        self.assertEqual(len(self.data_json['remote_resources']),
                         len(serialized_vinculum_data['remote_resources'])
                         )

        self.assertEqual(serialized_vinculum_data['remote_resources'][0]['remote_resource_path'],
                         self.remote_resource_path)

        self.assertEqual(len(self.data_json['remote_resources'][0]['io_paths']),
                         len(serialized_vinculum_data['remote_resources'][0]['io_paths'])
                         )

        self.assertEqual(serialized_vinculum_data['remote_resources'][0]['io_paths'][0]['input_path'],
                         "query.results.channel")
        self.assertEqual(serialized_vinculum_data['remote_resources'][0]['io_paths'][0]['output_path'],
                         "yahoo.weather")

    def test_was_vinculum_correctly_stored(self):

        response = self._login_post_vinculum()

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Vinculum.objects.count(), 1)
        self.assertEqual(RemoteResources.objects.count(), 1)
        self.assertEqual(InputOutputPath.objects.count(), 1)

        remoteresources = RemoteResources.objects.get(pk=1)
        self.assertEqual(remoteresources.remote_resource_path,
                         "https://query.yahooapis.com/v1/public/yql?q=select%20*%20from%20weather.forecast%20where%20woeid%20in%20(select%20woeid%20from%20geo.places(1)%20where%20text%3D%22nome%2C%20ak%22)&format=json&env=store%3A%2F%2Fdatatables.org%2Falltableswithkeys")
        self.assertEqual(remoteresources.authentication_behavior, "none")
        self.assertEqual(remoteresources.vinculum_id, 1)

        io_paths = InputOutputPath.objects.get(pk=1)
        self.assertEqual(io_paths.input_path, "query.results.channel")
        self.assertEqual(io_paths.output_path, "yahoo.weather")
        self.assertEqual(io_paths.remote_resource_id, 1)
