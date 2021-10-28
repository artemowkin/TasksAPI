from uuid import UUID

from django.test import TestCase
from django.contrib.auth import get_user_model
from django.utils import timezone

from ..models import Task


User = get_user_model()


class TaskModelTests(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser', password='testpass'
        )
        self.task = Task.objects.create(
            title='some task', subtitle='some subtitle', text='some text',
            owner=self.user
        )

    def test_created_task_fields(self):
        self.assertIsInstance(self.task.pk, UUID)
        self.assertEqual(self.task.title, 'some task')
        self.assertEqual(self.task.subtitle, 'some subtitle')
        self.assertEqual(self.task.text, 'some text')
        self.assertEqual(self.task.owner, self.user)
        self.assertEqual(self.task.pub_datetime.date(), timezone.now().date())

    def test_ordering(self):
        new_task = Task.objects.create(
            title='second task', subtitle='some subtitle', text='some text',
            owner=self.user
        )
        all_tasks = Task.objects.all()

        self.assertEqual(all_tasks.count(), 2)
        self.assertEqual(all_tasks[0], new_task)
        self.assertEqual(all_tasks[1], self.task)

    def test_string_representation(self):
        self.assertEqual(str(self.task), self.task.title)

