from django.test import TestCase, mock
from django.contrib.auth.models import User

from rest_framework.reverse import reverse

from email_devino.client import DevinoError, DevinoException

from .. import forms


class SendMessage(TestCase):
    def setUp(self):
        self.url = reverse('send_message_interface')
        self.user = User.objects.create(
            username='Test user',
            password='Test passwd'
        )

    @mock.patch('core.forms.DevinoClient.get_sender_addresses')
    def test_bad_answer_devino(self, mock_obj):
        mock_obj.side_effect = DevinoException(
            message='test',
            http_status=400,
            error=DevinoError(
                code=400,
                description='error'
            ),
        )
        form = forms.SendMessage()

        self.assertIn(('load_error', 'server is not available, reload the page'), form.fields['sender_email'].choices)
