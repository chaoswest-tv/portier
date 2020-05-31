from rest_framework_guardian.serializers import ObjectPermissionsAssignmentMixin
from rest_framework import serializers, viewsets
from rest_framework_guardian import filters
from rtmp.models import Application, Stream
from restream.models import RestreamConfig


class ApplicationSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Application
        fields = ['id', 'name']


class ApplicationViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Application.objects.all()
    serializer_class = ApplicationSerializer
    filter_backends = [filters.ObjectPermissionsFilter]


class StreamSerializer(ObjectPermissionsAssignmentMixin, serializers.ModelSerializer):
    class Meta:
        model = Stream
        fields = ['id', 'stream', 'name', 'application']

    def get_permissions_map(self, created):
        current_user = self.context['request'].user
        return {
            'view_stream': [current_user],
            'change_stream': [current_user],
            'delete_stream': [current_user]
        }


class StreamViewSet(viewsets.ModelViewSet):
    queryset = Stream.objects.all()
    serializer_class = StreamSerializer
    filter_backends = [filters.ObjectPermissionsFilter]


class RestreamConfigSerializer(ObjectPermissionsAssignmentMixin, serializers.ModelSerializer):
    class Meta:
        model = RestreamConfig
        fields = '__all__'

    def get_permissions_map(self, created):
        current_user = self.context['request'].user
        return {
            'view_restreamconfig': [current_user],
            'change_restreamconfig': [current_user],
            'delete_restreamconfig': [current_user]
        }

    def validate_stream(self, value):
        request = self.context['request']
        if not request.user.has_perm('rtmp.view_stream', value):
            raise serializers.ValidationError('Access to stream is not authorized')
        return value


class RestreamConfigViewSet(viewsets.ModelViewSet):
    queryset = RestreamConfig.objects.all()
    serializer_class = RestreamConfigSerializer
    filter_backends = [filters.ObjectPermissionsFilter]
