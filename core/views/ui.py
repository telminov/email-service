import json

from django.views.generic import FormView
from django.urls import reverse_lazy
from django.conf import settings
from django.contrib import messages
from django.views.generic import RedirectView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseBadRequest, HttpResponseRedirect

from email_devino.client import DevinoClient
from email_devino.client import DevinoException

from core import models
from core import forms
from core import consts


class Index(RedirectView):
    url = '/docs/'


class SendMessage(LoginRequiredMixin, FormView):
    login_url = reverse_lazy('login')
    redirect_field_name = reverse_lazy('send_message_interface')
    form_class = forms.SendMessage
    success_url = reverse_lazy('send_message_interface')
    template_name = 'core/send_message.html'

    def form_valid(self, form):
        json_data = json.dumps(form.cleaned_data)
        devino_request = models.DevinoRequest.objects.create(api_resource=consts.SEND_MESSAGE, data=json_data)

        try:
            answer = DevinoClient(settings.DEVINO_LOGIN, settings.DEVINO_PASSWORD).send_transactional_message(
                **form.cleaned_data)
            models.DevinoAnswer.objects.create(
                code=answer.code,
                description=answer.description,
                result=answer.result,
                request=devino_request,
            )
            messages.success(self.request, 'Message successfully delivered')
        except DevinoException as ex:
            models.DevinoAnswer.objects.create(
                code=ex.error.code,
                description=ex.error.description,
                request=devino_request,
                is_fail=True,
            )
            messages.error(self.request, 'Error in sending the request, pleate repeat')
            return HttpResponseBadRequest()
        return HttpResponseRedirect(self.success_url)
