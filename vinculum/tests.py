from django.contrib.auth.models import User
import json
import vcr

from .models import Vinculum, RemoteResources, InputOutputPath
from rest_framework.test import APITestCase
from rest_framework import status

from serializers import VinculumSerializer


class VinculumSerializeTest(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user('testuser', email='testuser@test.com', password='testing')
        self.user.save()
        self.data = {
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
        }
        self.data_string = json.dumps(self.data)
        self.data_json = json.loads(self.data_string)

        self.remote_resource_path = "https://query.yahooapis.com/v1/public/yql?q=select%20*%20from%20weather.forecast%20where%20woeid%20in%20(select%20woeid%20from%20geo.places(1)%20where%20text%3D%22nome%2C%20ak%22)&format=json&env=store%3A%2F%2Fdatatables.org%2Falltableswithkeys"

    def _require_login(self):
        self.client.login(username='testuser', password='testing')

    def _login_post_vinculum(self, data_to_post=None, cassette=None):

        self._require_login()

        if data_to_post is None:
            data_to_post = json.loads(self.data_string)

        response = self.client.post('/vinculums/', data_to_post, format='json')
        return response

    def _helper_deleted_blank_fields(self, field_to_test, post_vinculum):
        # TODO: Move this into a library for just itself
        data_to_post_deleted = self.data_json.copy()
        data_to_post_blank = self.data_json.copy()

        data_to_post_deleted.pop(field_to_test)
        response = post_vinculum(data_to_post_deleted)
        self.assertEqual(response.content,
                         '{"%s":["This field is required."]}' % field_to_test)

        data_to_post_blank[field_to_test] = None
        response = post_vinculum(data_to_post_blank)

        self.assertEqual(response.content,
                         '{"%s":["This field may not be null."]}' % field_to_test)

    def test_was_vinclum_correctly_serialized(self):

        response = self._login_post_vinculum()

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        vinculum_id = response.data['id']
        vinculum = Vinculum.objects.get(pk=vinculum_id)
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

    @vcr.use_cassette('test_artifacts/vcr_cassettes/was_vinculum_correctly_stored')
    def test_was_vinculum_correctly_stored(self):

        response = self._login_post_vinculum()

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        vinculum_id = response.data['id']

        self.assertEqual(Vinculum.objects.count(), 1)
        self.assertEqual(RemoteResources.objects.count(), 1)
        self.assertEqual(InputOutputPath.objects.count(), 1)

        remoteresources = RemoteResources.objects.all()[:1].get()
        self.assertEqual(remoteresources.remote_resource_path, self.remote_resource_path)
        self.assertEqual(remoteresources.authentication_behavior, "none")
        self.assertEqual(remoteresources.vinculum_id, vinculum_id)

        io_paths = InputOutputPath.objects.all()[:1].get()
        self.assertEqual(io_paths.input_path, "query.results.channel")
        self.assertEqual(io_paths.output_path, "yahoo.weather")
        self.assertEqual(io_paths.remote_resource_id, remoteresources.id)

    @vcr.use_cassette('test_artifacts/vcr_cassettes/vinculum_needs_root_path_missing')
    def test_vinculum_needs_root_path(self):
        # Test to see what happens when root_path is missing entirely

        field_to_test = 'root_path'

        data_to_post_deleted = json.loads(self.data_string)

        data_to_post_deleted.pop(field_to_test)

        response = self._login_post_vinculum(data_to_post_deleted)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.content,
                         '{"%s":["This field is required."]}' % field_to_test)

    @vcr.use_cassette('test_artifacts/vcr_cassettes/vinculum_needs_root_path_blank')
    def test_vinculum_needs_root_path_not_none(self):
        # what happens if root_path is present but none
        field_to_test = 'root_path'

        data_to_post_blank = self.data_json.copy()

        data_to_post_blank[field_to_test] = None
        response = self._login_post_vinculum(data_to_post_blank, cassette='test_artifacts/vcr_cassettes/vinculum_needs_root_path_blank')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        self.assertEqual(response.content,
                         '{"%s":["This field may not be null."]}' % field_to_test)

        self._helper_deleted_blank_fields('root_path',
                                          self._login_post_vinculum)

    @vcr.use_cassette('test_artifacts/vcr_cassettes/vinculum_needs_remote_resources_missing')
    def test_vinculum_needs_remote_resources(self):
        # test to see what happens when remote_resources is missing
        field_to_test = 'remote_resources'

        data_to_post_deleted = self.data_json.copy()

        data_to_post_deleted.pop(field_to_test)
        response = self._login_post_vinculum(data_to_post_deleted)
        self.assertEqual(response.content,
                         '{"%s":["This field is required."]}' % field_to_test)

    @vcr.use_cassette('test_artifacts/vcr_cassettes/vinculum_needs_remote_resources_blank')
    def test_vinculum_needs_remote_resources_blank(self):
        # test to see what happens when remote_resources is none

        field_to_test = 'remote_resources'

        data_to_post_blank = json.loads(self.data_string)

        data_to_post_blank[field_to_test] = None
        response = self._login_post_vinculum(data_to_post_blank)

        self.assertEqual(response.content,
                         '{"%s":["This field may not be null."]}' % field_to_test)

    @vcr.use_cassette('test_artifacts/vcr_cassettes/vinculum_is_running')
    def test_vinculum_is_running(self):

        response = self._login_post_vinculum()
        vinculum_id = response.data['id']
        vinculum = Vinculum.objects.get(pk=vinculum_id)
        self.assertTrue(isinstance(vinculum, Vinculum))

        response = self.client.get('/vinculums/' + str(vinculum_id) + '/running' , format='json')

        returned_data = response.json()
        self.assertTrue(response)
        self.assertTrue(response.status_code==200)
        self.assertTrue(returned_data['pk'] == '1')
        self.assertTrue(returned_data['running'] == True)