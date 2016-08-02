from rest_framework import serializers

from vinculum.models import Vinculum


class VinculumSerializer(serializers.ModelSerializer):

    owner = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model = Vinculum
        fields = ('id', 'title', 'input_paths', 'output_path', 'remote_resource', 'authentication', 'owner')

    def update(self, instance, validated_data):
        pass

    def create(self, validated_data):

        return Vinculum.objects.create(**validated_data)