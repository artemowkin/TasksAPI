from rest_framework import serializers

from .models import Task


class TaskSerializer(serializers.ModelSerializer):

    class Meta:
        model = Task
        fields = ('pk', 'title', 'subtitle', 'text')
        read_only_fields = ('pk',)

