from rest_framework import serializers

from .models import Task


class TaskSerializer(serializers.ModelSerializer):

    class Meta:
        model = Task
        fields = ('pk', 'title', 'subtitle', 'text', 'owner', 'pub_datetime')
        read_only_fields = ('pk', 'owner')

