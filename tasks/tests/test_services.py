from django.test import TestCase
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser
from django.core.exceptions import PermissionDenied
from django.http import Http404
from rest_framework.exceptions import ValidationError

from ..models import Task
from ..services import get_all_tasks, create_task, delete_task


User = get_user_model()


class GetAllTasksTests(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser', password='testpass'
        )
        self.task = Task.objects.create(
            title='some task', subtitle='some subtitle', text='some text',
            owner=self.user
        )

    def test_get_all_tasks_with_authenticated_user(self):
        all_user_tasks = get_all_tasks(self.user)
        self.assertEqual(all_user_tasks.count(), 1)
        self.assertEqual(all_user_tasks[0], self.task)

    def test_get_all_tasks_with_not_authenticated_user(self):
        with self.assertRaises(PermissionDenied):
            get_all_tasks(AnonymousUser())

    def test_get_all_tasks_with_another_user(self):
        new_user = User.objects.create_user(
            username='new_user', password='testpass'
        )
        all_user_tasks = get_all_tasks(new_user)
        self.assertEqual(all_user_tasks.count(), 0)


class CreateTaskTests(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser', password='testpass'
        )

    def test_create_with_authenticated_user(self):
        task = create_task(self.user, {
            'title': 'new task', 'subtitle': 'some subtitle',
            'text': 'some text'
        })

        self.assertEqual(task.title, 'new task')
        self.assertEqual(task.subtitle, 'some subtitle')
        self.assertEqual(task.text, 'some text')

    def test_create_with_not_authenticated_user(self):
        with self.assertRaises(PermissionDenied):
            create_task(AnonymousUser(), {
                'title': 'new task', 'subtitle': 'some subtitle',
                'text': 'some text'
            })

    def test_create_with_incorrect_data(self):
        with self.assertRaises(ValidationError):
            create_task(self.user, {'something': 'something'})


class DeleteTaskTests(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser', password='testpass'
        )
        self.task = Task.objects.create(
            title='some task', subtitle='some subtitle', text='some text',
            owner=self.user
        )

    def test_delete_with_task_author(self):
        delete_task(self.user, self.task.pk)
        self.assertEqual(Task.objects.count(), 0)

    def test_delete_with_another_user(self):
        new_user = User.objects.create_user(
            username='newuser', password='testpass'
        )
        with self.assertRaises(Http404):
            delete_task(new_user, self.task.pk)

    def test_delete_with_not_authenticated_user(self):
        with self.assertRaises(PermissionDenied):
            delete_task(AnonymousUser(), self.task.pk)

