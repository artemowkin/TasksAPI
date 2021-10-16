from uuid import uuid4

from django.db import models


class Task(models.Model):
    uuid = models.UUIDField(primary_key=True, editable=False, default=uuid4)
    title = models.CharField(max_length=100)
    subtitle = models.CharField(max_length=255)
    text = models.TextField()

    class Meta:
        db_table = 'tasks'
        ordering = ('title',)

    def __str__(self):
        return self.title

