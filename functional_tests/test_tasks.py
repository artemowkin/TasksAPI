from django.test import TestCase
from django.contrib.auth import get_user_model

from tasks.models import Task


User = get_user_model()


class TasksEndpointsTests(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser', password='testpass'
        )
        self.task = Task.objects.create(
            title='some task', subtitle='some task subtitle',
            text='some task text', owner=self.user
        )
        self.client.login(username='testuser', password='testpass')

    def test_get_all_tasks_with_authenticated_user(self):
        response = self.client.get('/tasks/')
        self.assertEqual(response.status_code, 200)
        json_response = response.json()
        task_pub_datetime = self.task.pub_datetime.strftime(
            '%Y-%m-%dT%H:%M:%S.%fZ'
        )
        self.assertEqual(json_response, [{
            'pk': str(self.task.pk), 'title': 'some task',
            'subtitle': 'some task subtitle', 'text': 'some task text',
            'owner': self.user.id,
            'pub_datetime': task_pub_datetime
        }])

    def test_get_all_tasks_with_unauthenticated_user(self):
        self.client.logout()
        response = self.client.get('/tasks/')
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.json(), {
            'detail': 'Authentication credentials were not provided.'
        })

    def test_get_all_tasks_returns_only_user_tasks(self):
        second_user = User.objects.create_user(
            username='seconduser', password='testpass'
        )
        second_task = Task.objects.create(
            title='second task', subtitle='some task subtitle',
            text='some task text', owner=second_user
        )
        response = self.client.get('/tasks/')
        self.assertEqual(response.status_code, 200)
        json_response = response.json()
        task_pub_datetime = self.task.pub_datetime.strftime(
            '%Y-%m-%dT%H:%M:%S.%fZ'
        )
        self.assertEqual(json_response, [{
            'pk': str(self.task.pk), 'title': 'some task',
            'subtitle': 'some task subtitle', 'text': 'some task text',
            'owner': self.user.id,
            'pub_datetime': task_pub_datetime
        }])

    def test_create_a_new_task_with_authenticated_user(self):
        response = self.client.post('/tasks/', {
            'title': 'second task', 'subtitle': 'some task subtitle',
            'text': 'some task text'
        }, content_type='application/json')
        self.assertEqual(response.status_code, 201)
        json_response = response.json()
        self.assertIn('pk', json_response)
        self.assertIn('pub_datetime', json_response)
        del json_response['pk']
        del json_response['pub_datetime']
        self.assertEqual(response.json(), {
            'title': 'second task',
            'subtitle': 'some task subtitle', 'text': 'some task text',
            'owner': self.user.id,
        })

    def test_create_a_new_task_with_not_authenticated_user(self):
        self.client.logout()
        response = self.client.post('/tasks/', {
            'title': 'second task', 'subtitle': 'some task subtitle',
            'text': 'some task text'
        }, content_type='application/json')
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.json(), {
            'detail': 'Authentication credentials were not provided.'
        })

    def test_delete_a_concrete_task_requesting_by_author_user(self):
        response = self.client.delete(f'/tasks/{self.task.pk}/')
        self.assertEqual(response.status_code, 204)

    def test_delete_with_not_authenticated_user(self):
        self.client.logout()
        response = self.client.delete(f'/tasks/{self.task.pk}/')
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.json(), {
            'detail': 'Authentication credentials were not provided.'
        })

    def test_delete_with_user_who_is_not_author_of_task(self):
        new_user = User.objects.create_user(
            username='newuser', password='testpass'
        )
        self.client.login(username='newuser', password='testpass')
        response = self.client.delete(f'/tasks/{self.task.pk}/')
        self.assertEqual(response.status_code, 404)

