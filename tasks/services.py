from uuid import UUID

from django.db.models import QuerySet, Model
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from django.core.exceptions import PermissionDenied

from .models import Task
from .serializers import TaskSerializer


User = get_user_model()


def _check_is_user_authenticated(user: User) -> None:
    """Check is user authenticated. If not raise PermissionDenied"""
    if not user.is_authenticated:
        raise PermissionDenied('User is not authenticated')


def get_all_tasks(user: User) -> QuerySet:
    """Get all user tasks"""
    _check_is_user_authenticated(user)
    return Task.objects.filter(owner=user)


def create_task(user: User, data: dict) -> Task:
    """Create a new task for user"""
    _check_is_user_authenticated(user)
    TaskSerializer(data=data).is_valid(raise_exception=True)
    task = Task.objects.create(owner=user, **data)
    return task


def get_concrete_task(user: User, pk: UUID) -> Task:
    """Get a concrete task using its pk"""
    _check_is_user_authenticated(user)
    task = get_object_or_404(Task, pk=pk, owner=user)
    return task


def delete_task(user: User, pk: UUID) -> None:
    """Delete user task"""
    task = get_concrete_task(user, pk)
    task.delete()

