from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

from ..models import Task


User = get_user_model()


class AllCreateTasksViewTests(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser', password='testpass'
        )
        self.client.login(username='testuser', password='testpass')

    def test_get(self):
        response = self.client.get(reverse('all_create_tasks'))
        self.assertEqual(response.status_code, 200)

    def test_post(self):
        response = self.client.post(reverse('all_create_tasks'), {
            'title': 'some task', 'subtitle': 'some subtitle',
            'text': 'some text'
        }, content_type='application/json')
        self.assertEqual(response.status_code, 201)


class DeleteTaskViewTests(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser', password='testpass'
        )
        self.client.login(username='testuser', password='testpass')
        self.task = Task.objects.create(
            title='some task', subtitle='some subtitle',
            text='some text', owner=self.user
        )

    def test_delete(self):
        response = self.client.delete(reverse(
            'delete_task', args=[str(self.task.pk)]
        ))
        self.assertEqual(response.status_code, 204)

