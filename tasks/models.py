from uuid import uuid4
from datetime import datetime

from django.db import models
from django.contrib.auth import get_user_model


User = get_user_model()


class Task(models.Model):
    uuid = models.UUIDField(primary_key=True, editable=False, default=uuid4)
    title = models.CharField(max_length=100)
    subtitle = models.CharField(max_length=255)
    text = models.TextField()
    owner = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='tasks', editable=False
    )
    pub_datetime = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'tasks'
        ordering = ('-pub_datetime', 'title')

    def __str__(self):
        return self.title

