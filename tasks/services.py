from uuid import UUID

from django.db.models import QuerySet
from django.shortcuts import get_object_or_404

from .models import Task


def get_all_tasks() -> QuerySet:
    return Task.objects.all()


def create_task(data: dict) -> Task:
    task = Task.objects.create(**data)
    return task


def delete_task(pk: UUID) -> None:
    task = get_object_or_404(Task, pk=pk)
    task.delete()

