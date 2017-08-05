import json
import datetime
import pytz

from django.test import mock
from django.contrib.auth.models import User

from rest_framework.test import APITestCase
from rest_framework import status
from rest_framework.reverse import reverse

from email_devino.client import DevinoError
from email_devino.client import ApiAnswer

from core import models
from core import consts
from core.views import rest
from core.utils import date_handler

ANSWER_SUCCESS = ApiAnswer.create({'Code': 'ok', 'Description': 'ok', 'Result': []})
ANSWER_VALIDATION_ERROR = ApiAnswer.create({'Code': 'validation_error', 'Description': 'validation_error',
                                            'Result': []})
ANSWER_INTERNAL_ERROR = ApiAnswer.create({'Code': 'internal_error', 'Description': 'internal_error',
                                          'Result': []})


class AuthMixin(object):
    def test_auth(self):
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class GetSenderAddresses(AuthMixin, APITestCase):
    def setUp(self):
        self.url = reverse('get_sender_addresses')
        self.user = User.objects.create(
            username='Test user',
            password='Test passwd'
        )

    def test_methods(self):
        self.client.force_authenticate(user=self.user)

        response_post = self.client.post(self.url)
        response_put = self.client.put(self.url)
        response_delete = self.client.delete(self.url)

        self.assertEqual(response_post.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
        self.assertEqual(response_put.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
        self.assertEqual(response_delete.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    @mock.patch('core.views.rest.GetSenderAddresses.api_resource_lib')
    def test_get_success(self, mock_obj):
        mock_obj.return_value = ANSWER_SUCCESS
        self.client.force_authenticate(user=self.user)

        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(models.DevinoRequest.objects.exists())
        self.assertEqual(models.DevinoRequest.objects.get().api_resource, consts.GET_SENDER_ADDRESSES)
        self.assertEqual(json.loads(models.DevinoRequest.objects.get().data), None)
        self.assertTrue(models.DevinoAnswer.objects.exists())
        self.assertFalse(models.DevinoAnswer.objects.get().is_fail)

    @mock.patch('core.views.rest.GetSenderAddresses.api_resource_lib')
    def test_get_error(self, mock_obj):
        mock_obj.side_effect = rest.DevinoException(
            message='test',
            http_status=400,
            error=DevinoError(
                code=400,
                description='error'
            ),
        )
        self.client.force_authenticate(user=self.user)

        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertTrue(models.DevinoRequest.objects.exists())
        self.assertEqual(models.DevinoRequest.objects.get().api_resource, consts.GET_SENDER_ADDRESSES)
        self.assertEqual(json.loads(models.DevinoRequest.objects.get().data), None)
        self.assertTrue(models.DevinoAnswer.objects.exists())
        self.assertTrue(models.DevinoAnswer.objects.get().is_fail)

    @mock.patch('core.views.rest.GetSenderAddresses.api_resource_lib')
    def test_get_validation_error(self, mock_obj):
        mock_obj.return_value = ANSWER_VALIDATION_ERROR
        self.client.force_authenticate(user=self.user)

        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    @mock.patch('core.views.rest.GetSenderAddresses.api_resource_lib')
    def test_get_internal_error(self, mock_obj):
        mock_obj.return_value = ANSWER_INTERNAL_ERROR
        self.client.force_authenticate(user=self.user)

        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_500_INTERNAL_SERVER_ERROR)


class AddSenderAddress(AuthMixin, APITestCase):
    def setUp(self):
        self.url = reverse('add_sender_address')
        self.user = User.objects.create(
            username='Test user',
            password='Test passwd'
        )

    def test_methods(self):
        self.client.force_authenticate(user=self.user)

        response_get = self.client.get(self.url)
        response_put = self.client.put(self.url)
        response_delete = self.client.delete(self.url)

        self.assertEqual(response_get.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
        self.assertEqual(response_put.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
        self.assertEqual(response_delete.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    @mock.patch('core.views.rest.AddSenderAddress.api_resource_lib')
    def test_add_success(self, mock_obj):
        mock_obj.return_value = ANSWER_SUCCESS
        self.client.force_authenticate(user=self.user)

        data = {'address': 'test@test.text'}
        response = self.client.post(self.url, data=data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(models.DevinoRequest.objects.exists())
        self.assertEqual(models.DevinoRequest.objects.get().api_resource, consts.ADD_SENDER_ADDRESS)
        self.assertEqual(json.loads(models.DevinoRequest.objects.get().data), data)
        self.assertTrue(models.DevinoAnswer.objects.exists())
        self.assertFalse(models.DevinoAnswer.objects.get().is_fail)

    @mock.patch('core.views.rest.AddSenderAddress.api_resource_lib')
    def test_add_error(self, mock_obj):
        mock_obj.side_effect = rest.DevinoException(
            message='test',
            http_status=400,
            error=DevinoError(
                code=400,
                description='error'
            ),
        )
        self.client.force_authenticate(user=self.user)

        data = {'address': 'test@test.text'}
        response = self.client.post(self.url, data=data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class DelSenderAddress(AuthMixin, APITestCase):
    def setUp(self):
        self.url = reverse('del_sender_address')
        self.user = User.objects.create(
            username='Test user',
            password='Test passwd'
        )

    def test_methods(self):
        self.client.force_authenticate(user=self.user)

        response_get = self.client.get(self.url)
        response_post = self.client.post(self.url)
        response_put = self.client.put(self.url)

        self.assertEqual(response_get.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
        self.assertEqual(response_post.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
        self.assertEqual(response_put.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    @mock.patch('core.views.rest.DelSenderAddress.api_resource_lib')
    def test_del_success(self, mock_obj):
        mock_obj.return_value = ANSWER_SUCCESS
        self.client.force_authenticate(user=self.user)

        data = {'address': 'test@test.text'}
        response = self.client.delete(self.url, data=data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(models.DevinoRequest.objects.exists())
        self.assertEqual(models.DevinoRequest.objects.get().api_resource, consts.DEL_SENDER_ADDRESS)
        self.assertEqual(json.loads(models.DevinoRequest.objects.get().data), data)
        self.assertTrue(models.DevinoAnswer.objects.exists())
        self.assertFalse(models.DevinoAnswer.objects.get().is_fail)

    @mock.patch('core.views.rest.DelSenderAddress.api_resource_lib')
    def test_del_error(self, mock_obj):
        mock_obj.side_effect = rest.DevinoException(
            message='test',
            http_status=400,
            error=DevinoError(
                code=400,
                description='error'
            ),
        )
        self.client.force_authenticate(user=self.user)

        data = {'address': 'test@test.text'}
        response = self.client.delete(self.url, data=data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class GetTasks(AuthMixin, APITestCase):
    def setUp(self):
        self.url = reverse('get_tasks')
        self.user = User.objects.create(
            username='Test user',
            password='Test passwd'
        )

    def test_methods(self):
        self.client.force_authenticate(user=self.user)

        response_post = self.client.post(self.url)
        response_put = self.client.put(self.url)
        response_delete = self.client.delete(self.url)

        self.assertEqual(response_post.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
        self.assertEqual(response_put.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
        self.assertEqual(response_delete.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    @mock.patch('core.views.rest.GetTasks.api_resource_lib')
    def test_get_success(self, mock_obj):
        mock_obj.return_value = ANSWER_SUCCESS
        self.client.force_authenticate(user=self.user)

        data = {'range_start': 1, 'range_end': 100}
        response = self.client.get(self.url, data=data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(models.DevinoRequest.objects.exists())
        self.assertEqual(models.DevinoRequest.objects.get().api_resource, consts.GET_TASKS_LIST)
        self.assertEqual(json.loads(models.DevinoRequest.objects.get().data), data)
        self.assertTrue(models.DevinoAnswer.objects.exists())
        self.assertFalse(models.DevinoAnswer.objects.get().is_fail)

    @mock.patch('core.views.rest.GetTasks.api_resource_lib')
    def test_get_error(self, mock_obj):
        mock_obj.side_effect = rest.DevinoException(
            message='test',
            http_status=400,
            error=DevinoError(
                code=400,
                description='error'
            ),
        )
        self.client.force_authenticate(user=self.user)

        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class GetTask(AuthMixin, APITestCase):
    def setUp(self):
        self.url = reverse('get_task')
        self.user = User.objects.create(
            username='Test user',
            password='Test passwd'
        )

    def test_methods(self):
        self.client.force_authenticate(user=self.user)

        response_post = self.client.post(self.url)
        response_put = self.client.put(self.url)
        response_delete = self.client.delete(self.url)

        self.assertEqual(response_post.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
        self.assertEqual(response_put.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
        self.assertEqual(response_delete.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    @mock.patch('core.views.rest.GetTask.api_resource_lib')
    def test_get_success(self, mock_obj):
        mock_obj.return_value = ANSWER_SUCCESS
        self.client.force_authenticate(user=self.user)

        data = {'id_task': 1}
        response = self.client.get(self.url, data=data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(models.DevinoRequest.objects.exists())
        self.assertEqual(models.DevinoRequest.objects.get().api_resource, consts.GET_TASK)
        self.assertEqual(json.loads(models.DevinoRequest.objects.get().data), data)
        self.assertTrue(models.DevinoAnswer.objects.exists())
        self.assertFalse(models.DevinoAnswer.objects.get().is_fail)

    @mock.patch('core.views.rest.GetTask.api_resource_lib')
    def test_get_error(self, mock_obj):
        mock_obj.side_effect = rest.DevinoException(
            message='test',
            http_status=400,
            error=DevinoError(
                code=400,
                description='error'
            ),
        )
        self.client.force_authenticate(user=self.user)

        data = {'id_task': 1}
        response = self.client.get(self.url, data=data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class AddTask(AuthMixin, APITestCase):
    def setUp(self):
        self.url = reverse('add_task')
        self.user = User.objects.create(
            username='Test user',
            password='Test passwd'
        )

    def test_methods(self):
        self.client.force_authenticate(user=self.user)

        response_get = self.client.get(self.url)
        response_put = self.client.put(self.url)
        response_delete = self.client.delete(self.url)

        self.assertEqual(response_get.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
        self.assertEqual(response_put.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
        self.assertEqual(response_delete.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    @mock.patch('core.views.rest.AddTask.api_resource_lib')
    def test_post_success(self, mock_obj):
        mock_obj.return_value = ANSWER_SUCCESS
        self.client.force_authenticate(user=self.user)

        data = {'name': 'test', 'sender_email': 'test@test.test', 'sender_name': 'test name',
                'subject': 'test subj', 'text': 'test text', 'type_task': 1,
                'start': datetime.datetime(year=2017, month=8, day=1, tzinfo=pytz.UTC),
                'end': datetime.datetime(year=2017, month=9, day=1, tzinfo=pytz.UTC),
                'user_id': '1234', 'template_id': '1234', 'duplicates': True}

        response = self.client.post(self.url, data)
        data['contact_list'] = []
        data['start'] = json.loads(json.dumps(data['start'], default=date_handler))
        data['end'] = json.loads(json.dumps(data['end'], default=date_handler))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(models.DevinoRequest.objects.exists())
        self.assertEqual(models.DevinoRequest.objects.get().api_resource, consts.ADD_TASK)
        self.assertEqual(json.loads(models.DevinoRequest.objects.get().data), data)
        self.assertTrue(models.DevinoAnswer.objects.exists())
        self.assertFalse(models.DevinoAnswer.objects.get().is_fail)

    @mock.patch('core.views.rest.AddTask.api_resource_lib')
    def test_get_error(self, mock_obj):
        mock_obj.side_effect = rest.DevinoException(
            message='test',
            http_status=400,
            error=DevinoError(
                code=400,
                description='error'
            ),
        )
        self.client.force_authenticate(user=self.user)

        data = {'name': 'test', 'sender_email': 'test@test.test', 'sender_name': 'test name',
                'subject': 'test subj', 'text': 'test text', 'type_task': 1,
                'start': datetime.datetime(year=2017, month=8, day=1, tzinfo=pytz.UTC),
                'end': datetime.datetime(year=2017, month=9, day=1, tzinfo=pytz.UTC),
                'user_id': '1234', 'template_id': '1234', 'duplicates': True}
        response = self.client.post(self.url, data=data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class EditTask(AuthMixin, APITestCase):
    def setUp(self):
        self.url = reverse('edit_task')
        self.user = User.objects.create(
            username='Test user',
            password='Test passwd'
        )

    def test_methods(self):
        self.client.force_authenticate(user=self.user)

        response_get = self.client.get(self.url)
        response_post = self.client.post(self.url)
        response_delete = self.client.delete(self.url)

        self.assertEqual(response_get.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
        self.assertEqual(response_post.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
        self.assertEqual(response_delete.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    @mock.patch('core.views.rest.EditTask.api_resource_lib')
    def test_post_success(self, mock_obj):
        mock_obj.return_value = ANSWER_SUCCESS
        self.client.force_authenticate(user=self.user)

        data = {'id_task': 1, 'name': 'test', 'sender_email': 'test@test.test', 'sender_name': 'test name',
                'subject': 'test subj', 'text': 'test text', 'type_task': 1,
                'start': datetime.datetime(year=2017, month=8, day=1, tzinfo=pytz.UTC),
                'end': datetime.datetime(year=2017, month=9, day=1, tzinfo=pytz.UTC),
                'user_id': '1234', 'template_id': '1234', 'duplicates': True}

        response = self.client.put(self.url, data)
        data['contact_list'] = []
        data['start'] = json.loads(json.dumps(data['start'], default=date_handler))
        data['end'] = json.loads(json.dumps(data['end'], default=date_handler))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(models.DevinoRequest.objects.exists())
        self.assertEqual(models.DevinoRequest.objects.get().api_resource, consts.EDIT_TASK)
        self.assertEqual(json.loads(models.DevinoRequest.objects.get().data), data)
        self.assertTrue(models.DevinoAnswer.objects.exists())
        self.assertFalse(models.DevinoAnswer.objects.get().is_fail)

    @mock.patch('core.views.rest.EditTask.api_resource_lib')
    def test_get_error(self, mock_obj):
        mock_obj.side_effect = rest.DevinoException(
            message='test',
            http_status=400,
            error=DevinoError(
                code=400,
                description='error'
            ),
        )
        self.client.force_authenticate(user=self.user)

        data = {'id_task': 1, 'name': 'test', 'sender_email': 'test@test.test', 'sender_name': 'test name',
                'subject': 'test subj', 'text': 'test text', 'type_task': 1,
                'start': datetime.datetime(year=2017, month=8, day=1, tzinfo=pytz.UTC),
                'end': datetime.datetime(year=2017, month=9, day=1, tzinfo=pytz.UTC),
                'user_id': '1234', 'template_id': '1234', 'duplicates': True}
        response = self.client.put(self.url, data=data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class EditTaskStatus(AuthMixin, APITestCase):
    def setUp(self):
        self.url = reverse('edit_task_status')
        self.user = User.objects.create(
            username='Test user',
            password='Test passwd'
        )

    def test_methods(self):
        self.client.force_authenticate(user=self.user)

        response_get = self.client.get(self.url)
        response_post = self.client.post(self.url)
        response_delete = self.client.delete(self.url)

        self.assertEqual(response_get.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
        self.assertEqual(response_post.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
        self.assertEqual(response_delete.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    @mock.patch('core.views.rest.EditTaskStatus.api_resource_lib')
    def test_post_success(self, mock_obj):
        mock_obj.return_value = ANSWER_SUCCESS
        self.client.force_authenticate(user=self.user)

        data = {'id_task': 1, 'task_state': '1'}

        response = self.client.put(self.url, data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(models.DevinoRequest.objects.exists())
        self.assertEqual(models.DevinoRequest.objects.get().api_resource, consts.EDIT_TASK_STATUS)
        self.assertEqual(json.loads(models.DevinoRequest.objects.get().data), data)
        self.assertTrue(models.DevinoAnswer.objects.exists())
        self.assertFalse(models.DevinoAnswer.objects.get().is_fail)

    @mock.patch('core.views.rest.EditTaskStatus.api_resource_lib')
    def test_get_error(self, mock_obj):
        mock_obj.side_effect = rest.DevinoException(
            message='test',
            http_status=400,
            error=DevinoError(
                code=400,
                description='error'
            ),
        )
        self.client.force_authenticate(user=self.user)

        data = {'id_task': 1, 'task_state': 1}
        response = self.client.put(self.url, data=data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class GetTemplate(AuthMixin, APITestCase):
    def setUp(self):
        self.url = reverse('get_template')
        self.user = User.objects.create(
            username='Test user',
            password='Test passwd'
        )

    def test_methods(self):
        self.client.force_authenticate(user=self.user)

        response_post = self.client.post(self.url)
        response_put = self.client.put(self.url)
        response_delete = self.client.delete(self.url)

        self.assertEqual(response_post.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
        self.assertEqual(response_put.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
        self.assertEqual(response_delete.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    @mock.patch('core.views.rest.GetTemplate.api_resource_lib')
    def test_get_success(self, mock_obj):
        mock_obj.return_value = ANSWER_SUCCESS
        self.client.force_authenticate(user=self.user)

        data = {'id_template': 1}
        response = self.client.get(self.url, data=data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(models.DevinoRequest.objects.exists())
        self.assertEqual(models.DevinoRequest.objects.get().api_resource, consts.GET_TEMPLATE)
        self.assertEqual(json.loads(models.DevinoRequest.objects.get().data), data)
        self.assertTrue(models.DevinoAnswer.objects.exists())
        self.assertFalse(models.DevinoAnswer.objects.get().is_fail)

    @mock.patch('core.views.rest.GetTemplate.api_resource_lib')
    def test_get_error(self, mock_obj):
        mock_obj.side_effect = rest.DevinoException(
            message='test',
            http_status=400,
            error=DevinoError(
                code=400,
                description='error'
            ),
        )
        self.client.force_authenticate(user=self.user)

        data = {'id_template': 1}
        response = self.client.get(self.url, data=data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class AddTemplate(AuthMixin, APITestCase):
    def setUp(self):
        self.url = reverse('add_template')
        self.user = User.objects.create(
            username='Test user',
            password='Test passwd'
        )

    def test_methods(self):
        self.client.force_authenticate(user=self.user)

        response_get = self.client.get(self.url)
        response_put = self.client.put(self.url)
        response_delete = self.client.delete(self.url)

        self.assertEqual(response_get.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
        self.assertEqual(response_put.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
        self.assertEqual(response_delete.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    @mock.patch('core.views.rest.AddTemplate.api_resource_lib')
    def test_post_success(self, mock_obj):
        mock_obj.return_value = ANSWER_SUCCESS
        self.client.force_authenticate(user=self.user)

        data = {'name': 'test', 'sender_email': 'test@test.test', 'sender_name': 'test name',
                'subject': 'test subj', 'text': 'test text', 'user_template_id': '123ew3'}

        response = self.client.post(self.url, data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(models.DevinoRequest.objects.exists())
        self.assertEqual(models.DevinoRequest.objects.get().api_resource, consts.ADD_TEMPLATE)
        self.assertEqual(json.loads(models.DevinoRequest.objects.get().data), data)
        self.assertTrue(models.DevinoAnswer.objects.exists())
        self.assertFalse(models.DevinoAnswer.objects.get().is_fail)

    @mock.patch('core.views.rest.AddTemplate.api_resource_lib')
    def test_get_error(self, mock_obj):
        mock_obj.side_effect = rest.DevinoException(
            message='test',
            http_status=400,
            error=DevinoError(
                code=400,
                description='error'
            ),
        )
        self.client.force_authenticate(user=self.user)

        data = {'name': 'test', 'sender_email': 'test@test.test', 'sender_name': 'test name',
                'subject': 'test subj', 'text': 'test text', 'user_template_id': '123ew3'}

        response = self.client.post(self.url, data=data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class EditTemplate(AuthMixin, APITestCase):
    def setUp(self):
        self.url = reverse('edit_template')
        self.user = User.objects.create(
            username='Test user',
            password='Test passwd'
        )

    def test_methods(self):
        self.client.force_authenticate(user=self.user)

        response_get = self.client.get(self.url)
        response_post = self.client.post(self.url)
        response_delete = self.client.delete(self.url)

        self.assertEqual(response_get.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
        self.assertEqual(response_post.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
        self.assertEqual(response_delete.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    @mock.patch('core.views.rest.EditTemplate.api_resource_lib')
    def test_post_success(self, mock_obj):
        mock_obj.return_value = ANSWER_SUCCESS
        self.client.force_authenticate(user=self.user)

        data = {'id_template': 1, 'name': 'test', 'sender_email': 'test@test.test', 'sender_name': 'test name',
                'subject': 'test subj', 'text': 'test text', 'user_template_id': '123ew3'}

        response = self.client.put(self.url, data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(models.DevinoRequest.objects.exists())
        self.assertEqual(models.DevinoRequest.objects.get().api_resource, consts.EDIT_TEMPLATE)
        self.assertEqual(json.loads(models.DevinoRequest.objects.get().data), data)
        self.assertTrue(models.DevinoAnswer.objects.exists())
        self.assertFalse(models.DevinoAnswer.objects.get().is_fail)

    @mock.patch('core.views.rest.EditTemplate.api_resource_lib')
    def test_get_error(self, mock_obj):
        mock_obj.side_effect = rest.DevinoException(
            message='test',
            http_status=400,
            error=DevinoError(
                code=400,
                description='error'
            ),
        )
        self.client.force_authenticate(user=self.user)

        data = {'id_template': 1, 'name': 'test', 'sender_email': 'test@test.test', 'sender_name': 'test name',
                'subject': 'test subj', 'text': 'test text', 'user_template_id': '123ew3'}

        response = self.client.put(self.url, data=data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class DelTemplate(AuthMixin, APITestCase):
    def setUp(self):
        self.url = reverse('del_template')
        self.user = User.objects.create(
            username='Test user',
            password='Test passwd'
        )

    def test_methods(self):
        self.client.force_authenticate(user=self.user)

        response_get = self.client.get(self.url)
        response_post = self.client.post(self.url)
        response_put = self.client.put(self.url)

        self.assertEqual(response_get.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
        self.assertEqual(response_post.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
        self.assertEqual(response_put.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    @mock.patch('core.views.rest.DelTemplate.api_resource_lib')
    def test_del_success(self, mock_obj):
        mock_obj.return_value = ANSWER_SUCCESS
        self.client.force_authenticate(user=self.user)

        data = {'id_template': 1}
        response = self.client.delete(self.url, data=data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(models.DevinoRequest.objects.exists())
        self.assertEqual(models.DevinoRequest.objects.get().api_resource, consts.DEL_TEMPLATE)
        self.assertEqual(json.loads(models.DevinoRequest.objects.get().data), data)
        self.assertTrue(models.DevinoAnswer.objects.exists())
        self.assertFalse(models.DevinoAnswer.objects.get().is_fail)

    @mock.patch('core.views.rest.DelTemplate.api_resource_lib')
    def test_del_error(self, mock_obj):
        mock_obj.side_effect = rest.DevinoException(
            message='test',
            http_status=400,
            error=DevinoError(
                code=400,
                description='error'
            ),
        )
        self.client.force_authenticate(user=self.user)

        data = {'id_template': 1}
        response = self.client.delete(self.url, data=data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class GetState(AuthMixin, APITestCase):
    def setUp(self):
        self.url = reverse('get_state')
        self.user = User.objects.create(
            username='Test user',
            password='Test passwd'
        )

    def test_methods(self):
        self.client.force_authenticate(user=self.user)

        response_post = self.client.post(self.url)
        response_put = self.client.put(self.url)
        response_delete = self.client.delete(self.url)

        self.assertEqual(response_post.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
        self.assertEqual(response_put.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
        self.assertEqual(response_delete.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    @mock.patch('core.views.rest.GetState.api_resource_lib')
    def test_get_success(self, mock_obj):
        mock_obj.return_value = ANSWER_SUCCESS
        self.client.force_authenticate(user=self.user)

        data = {'id_task': 1}
        response = self.client.get(self.url, data=data)
        data['start'] = None
        data['end'] = None

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(models.DevinoRequest.objects.exists())
        self.assertEqual(models.DevinoRequest.objects.get().api_resource, consts.GET_STATE)
        self.assertEqual(json.loads(models.DevinoRequest.objects.get().data), data)
        self.assertTrue(models.DevinoAnswer.objects.exists())
        self.assertFalse(models.DevinoAnswer.objects.get().is_fail)

    @mock.patch('core.views.rest.GetState.api_resource_lib')
    def test_get_error(self, mock_obj):
        mock_obj.side_effect = rest.DevinoException(
            message='test',
            http_status=400,
            error=DevinoError(
                code=400,
                description='error'
            ),
        )
        self.client.force_authenticate(user=self.user)

        data = {'id_task': 1}
        response = self.client.get(self.url, data=data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class GetStateDetailing(AuthMixin, APITestCase):
    def setUp(self):
        self.url = reverse('get_state_detailing')
        self.user = User.objects.create(
            username='Test user',
            password='Test passwd'
        )

    def test_methods(self):
        self.client.force_authenticate(user=self.user)

        response_post = self.client.post(self.url)
        response_put = self.client.put(self.url)
        response_delete = self.client.delete(self.url)

        self.assertEqual(response_post.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
        self.assertEqual(response_put.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
        self.assertEqual(response_delete.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    @mock.patch('core.views.rest.GetStateDetailing.api_resource_lib')
    def test_get_success(self, mock_obj):
        mock_obj.return_value = ANSWER_SUCCESS
        self.client.force_authenticate(user=self.user)

        data = {'id_task': 1}
        response = self.client.get(self.url, data=data)
        data['start'] = None
        data['end'] = None
        data['state'] = None
        data['range_start'] = 1
        data['range_end'] = 100

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(models.DevinoRequest.objects.exists())
        self.assertEqual(models.DevinoRequest.objects.get().api_resource, consts.GET_STATE_DETAILING)
        self.assertEqual(json.loads(models.DevinoRequest.objects.get().data), data)
        self.assertTrue(models.DevinoAnswer.objects.exists())
        self.assertFalse(models.DevinoAnswer.objects.get().is_fail)

    @mock.patch('core.views.rest.GetStateDetailing.api_resource_lib')
    def test_get_error(self, mock_obj):
        mock_obj.side_effect = rest.DevinoException(
            message='test',
            http_status=400,
            error=DevinoError(
                code=400,
                description='error'
            ),
        )
        self.client.force_authenticate(user=self.user)

        data = {'id_task': 1}
        response = self.client.get(self.url, data=data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class SendMessage(AuthMixin, APITestCase):
    def setUp(self):
        self.url = reverse('send_message')
        self.user = User.objects.create(
            username='Test user',
            password='Test passwd'
        )

    def test_methods(self):
        self.client.force_authenticate(user=self.user)

        response_get = self.client.get(self.url)
        response_put = self.client.put(self.url)
        response_delete = self.client.delete(self.url)

        self.assertEqual(response_get.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
        self.assertEqual(response_put.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
        self.assertEqual(response_delete.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    @mock.patch('core.views.rest.SendMessage.api_resource_lib')
    def test_post_success(self, mock_obj):
        mock_obj.return_value = ANSWER_SUCCESS
        self.client.force_authenticate(user=self.user)

        data = {'sender_email': 'test@test.test', 'sender_name': 'test name',
                'recipient_email': 'othertest@test.test', 'recipient_name': 'test rec name',
                'subject': 'test subj', 'text': 'test text', 'user_message_id': '123ew3', 'user_campaign_id': '124ew4',
                'template_id': '1234'}

        response = self.client.post(self.url, data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(models.DevinoRequest.objects.exists())
        self.assertEqual(models.DevinoRequest.objects.get().api_resource, consts.SEND_MESSAGE)
        self.assertEqual(json.loads(models.DevinoRequest.objects.get().data), data)
        self.assertTrue(models.DevinoAnswer.objects.exists())
        self.assertFalse(models.DevinoAnswer.objects.get().is_fail)

    @mock.patch('core.views.rest.SendMessage.api_resource_lib')
    def test_get_error(self, mock_obj):
        mock_obj.side_effect = rest.DevinoException(
            message='test',
            http_status=400,
            error=DevinoError(
                code=400,
                description='error'
            ),
        )
        self.client.force_authenticate(user=self.user)

        data = {'sender_email': 'test@test.test', 'sender_name': 'test name',
                'recipient_email': 'othertest@test.test', 'recipient_name': 'test rec name',
                'subject': 'test subj', 'text': 'test text', 'user_message_id': '123ew3', 'user_campaign_id': '124ew4',
                'template_id': '1234'}

        response = self.client.post(self.url, data=data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class GetStatusMessages(AuthMixin, APITestCase):
    def setUp(self):
        self.url = reverse('get_status_messages')
        self.user = User.objects.create(
            username='Test user',
            password='Test passwd'
        )

    def test_methods(self):
        self.client.force_authenticate(user=self.user)

        response_post = self.client.post(self.url)
        response_put = self.client.put(self.url)
        response_delete = self.client.delete(self.url)

        self.assertEqual(response_post.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
        self.assertEqual(response_put.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
        self.assertEqual(response_delete.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    @mock.patch('core.views.rest.GetStatusMessages.api_resource_lib')
    def test_get_success(self, mock_obj):
        mock_obj.return_value = ANSWER_SUCCESS
        self.client.force_authenticate(user=self.user)

        data = {'id_messages': ['e2wfr3', 'sfd24f']}
        response = self.client.get(self.url, data=data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(models.DevinoRequest.objects.exists())
        self.assertEqual(models.DevinoRequest.objects.get().api_resource, consts.GET_STATUS_MESSAGE)
        self.assertEqual(json.loads(models.DevinoRequest.objects.get().data), data)
        self.assertTrue(models.DevinoAnswer.objects.exists())
        self.assertFalse(models.DevinoAnswer.objects.get().is_fail)

    @mock.patch('core.views.rest.GetStatusMessages.api_resource_lib')
    def test_get_error(self, mock_obj):
        mock_obj.side_effect = rest.DevinoException(
            message='test',
            http_status=400,
            error=DevinoError(
                code=400,
                description='error'
            ),
        )
        self.client.force_authenticate(user=self.user)

        data = {'id_messages': ['e2wfr3', 'sfd24f']}
        response = self.client.get(self.url, data=data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
