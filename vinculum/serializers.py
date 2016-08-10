from rest_framework import serializers

from vinculum.models import Vinculum, RemoteResources, InputOutputPath


class InputOutputPathSerializer(serializers.ModelSerializer):

    class Meta:
        model = InputOutputPath
        fields = ("input_path", "output_path")


class RemoteResourceSerializer(serializers.ModelSerializer):
    io_paths = InputOutputPathSerializer(many=True)

    class Meta:
        model = RemoteResources
        fields = ('authentication_behavior', 'remote_resource_path', 'io_paths')

    # def create(self, validated_data):
    #     input_paths = validated_data.pop('input_paths')
    #     remote_resource = RemoteResources.objects.create(**validated_data)
    #     for input_path in input_paths:
    #         InputPath.objects.create(remote_resource=remote_resource, **input_path)
    #     return remote_resource


class VinculumSerializer(serializers.ModelSerializer):

    owner = serializers.ReadOnlyField(source='owner.username')
    remote_resources = RemoteResourceSerializer(many=True)

    class Meta:
        model = Vinculum
        fields = ('id', 'title', 'owner', "root_path", "remote_resources")

    def create(self, validated_data):
        # manually buildup the entire vinculum here. Newer versions of DRF don't
        # support automatic deserialization nested anymore
        remoteresources = validated_data.pop('remote_resources')
        vinculum = Vinculum.objects.create(**validated_data)
        for remoteresource in remoteresources:
            io_paths = remoteresource.pop('io_paths')
            r = RemoteResources.objects.create(vinculum=vinculum, **remoteresource)
            for io_path in io_paths:
                InputOutputPath.objects.create(remote_resource=r, **io_path)
        return vinculum

    # def update(self, instance, validated_data):
    #     # manually buildup the entire
    #     remoteresources = validated_data.pop('remote_resources')
    #     for remoteresource in remoteresources:
    #         pass
    #     return instance