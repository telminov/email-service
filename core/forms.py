from django import forms
from django.conf import settings

from email_devino.client import DevinoClient
from email_devino.client import DevinoException


class SendMessage(forms.Form):
    recipient_name = forms.CharField()
    recipient_email = forms.EmailField()
    sender_email = forms.ChoiceField(widget=forms.Select, choices=[('server is not available, reload the page',
                                                                    'server is not available, reload the page')])
    sender_name = forms.CharField()
    subject = forms.CharField()
    text = forms.CharField()
    user_message_id = forms.CharField(required=False)
    user_campaign_id = forms.CharField(required=False)
    template_id = forms.CharField(required=False)

    def __init__(self, *args, **kwargs):
        super(SendMessage, self).__init__(*args, **kwargs)

        try:
            answer = DevinoClient(settings.DEVINO_LOGIN, settings.DEVINO_PASSWORD).get_addresses_sender()
            emails = []

            for data in answer.result:
                if data['Confirmed'] is True:
                    emails.append(data['SenderAddress'])

            emails = [(email, email) for email in emails]
            self.fields['sender_email'].choices = emails

        except DevinoException:
            pass
