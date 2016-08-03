from rest_framework import serializers

from vinculum.models import Vinculum, RemoteResources


class RemoteResourceSerializer(serializers.ModelSerializer):
    class Meta:
        model = RemoteResources
        fields = ('id', 'authentication_behavior', 'remote_resource_path', 'output_path')


class VinculumSerializer(serializers.ModelSerializer):

    owner = serializers.ReadOnlyField(source='owner.username')
    remote_resources = RemoteResourceSerializer(many=True)

    class Meta:
        model = Vinculum
        fields = ('id', 'title', 'owner', "root_path", "remote_resources")

    def create(self, validated_data):
        remoteresources = validated_data.pop('remote_resources')
        vinculum = Vinculum.objects.create(**validated_data)
        for remoteresource in remoteresources:
            RemoteResources.objects.create(vinculum=vinculum, **remoteresource)
        return vinculum

