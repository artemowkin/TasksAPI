from uuid import UUID

from django.db.models import QuerySet
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model

from .models import Task


User = get_user_model()


def get_all_tasks(user: User) -> QuerySet:
    return Task.objects.filter(owner=user)


def create_task(user: User, data: dict) -> Task:
    task = Task.objects.create(owner=user, **data)
    return task


def delete_task(user: User, pk: UUID) -> None:
    task = get_object_or_404(Task, pk=pk, owner=user)
    task.delete()

