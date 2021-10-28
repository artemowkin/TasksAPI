from uuid import UUID

from django.db.models import QuerySet
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from django.core.exceptions import PermissionDenied

from .models import Task


User = get_user_model()


def _check_is_user_authenticated(user: User):
    if not user.is_authenticated:
        raise PermissionDenied('User is not authenticated')


def get_all_tasks(user: User) -> QuerySet:
    _check_is_user_authenticated(user)
    return Task.objects.filter(owner=user)


def create_task(user: User, data: dict) -> Task:
    _check_is_user_authenticated(user)
    task = Task.objects.create(owner=user, **data)
    return task


def delete_task(user: User, pk: UUID) -> None:
    _check_is_user_authenticated(user)
    task = get_object_or_404(Task, pk=pk, owner=user)
    task.delete()

