import json

from django.test import TestCase, mock
from django.contrib.auth.models import User

from rest_framework import status
from rest_framework.reverse import reverse

from email_devino.client import DevinoError
from email_devino.client import ApiAnswer

from .. import models
from .. import consts
from ..views import rest

ANSWER_SUCCESS = ApiAnswer.create({'Code': 'ok', 'Description': 'ok', 'Result': []})


class UiSendMessage(TestCase):
    def setUp(self):
        self.url = reverse('send_message_interface')
        self.user = User.objects.create(
            username='Test user',
            password='Test passwd'
        )

    def test_auth(self):

        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_302_FOUND)

    @mock.patch('core.views.ui.DevinoClient.get_sender_addresses')
    @mock.patch('core.views.ui.DevinoClient.send_transactional_message')
    def test_post_success(self, mock_obj_send, mock_obj_get):
        mock_obj_get.return_value = ApiAnswer.create({'Result': [{'SenderAddress': 'test@test.test',
                                                                  'Confirmed': True}]})
        mock_obj_send.return_value = ANSWER_SUCCESS
        self.client.force_login(user=self.user)

        data = {'sender_email': 'test@test.test', 'sender_name': 'test name',
                'recipient_email': 'othertest@test.test', 'recipient_name': 'test rec name',
                'subject': 'test subj', 'text': 'test text', 'user_message_id': '123ew3', 'user_campaign_id': '124ew4',
                'template_id': '1234'}

        response = self.client.post(self.url, data)

        self.assertTrue(models.DevinoRequest.objects.exists())
        self.assertEqual(models.DevinoRequest.objects.get().api_resource, consts.SEND_MESSAGE)
        self.assertEqual(json.loads(models.DevinoRequest.objects.get().data), data)
        self.assertTrue(models.DevinoAnswer.objects.exists())
        self.assertFalse(models.DevinoAnswer.objects.get().is_fail)
        self.assertRedirects(response, self.url)

    @mock.patch('core.views.ui.DevinoClient.get_sender_addresses')
    @mock.patch('core.views.ui.DevinoClient.send_transactional_message')
    def test_get_error(self, mock_obj_send, mock_obj_get):
        mock_obj_get.return_value = ApiAnswer.create({'Result': [{'SenderAddress': 'test@test.test',
                                                                  'Confirmed': True}]})
        mock_obj_send.side_effect = rest.DevinoException(
            message='test',
            http_status=400,
            error=DevinoError(
                code=400,
                description='error'
            ),
        )
        self.client.force_login(user=self.user)

        data = {'sender_email': 'test@test.test', 'sender_name': 'test name',
                'recipient_email': 'othertest@test.test', 'recipient_name': 'test rec name',
                'subject': 'test subj', 'text': 'test text', 'user_message_id': '123ew3', 'user_campaign_id': '124ew4',
                'template_id': '1234'}

        response = self.client.post(self.url, data=data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
