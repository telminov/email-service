import json

from django.conf import settings
from rest_framework import views
from rest_framework.response import Response
from rest_framework import status

from email_devino.client import DevinoClient
from email_devino.client import DevinoException

from . import models
from . import consts
from . import serializers


class GetAddressesSender(views.APIView):
    def get(self, request):
        client = DevinoClient(settings.DEVINO_LOGIN, settings.DEVINO_PASSWORD)
        devino_request = models.DevinoRequest.objects.create(api=consts.GET_ADDRESSES_SENDER)
        try:
            answer = client.get_addresses_sender()
            models.DevinoAnswer.objects.create(
                code=answer.code,
                description=answer.description,
                result=answer.result,
                request=devino_request,
            )
            return Response(answer.result)
        except DevinoException as ex:
            error_serializer = serializers.DevinoError.register_exception(devino_request, ex)
            return Response(error_serializer.data, status=status.HTTP_400_BAD_REQUEST)


class AddAddressSender(views.APIView):
    def post(self, request):
        serializer = serializers.AddressSender(data=request.data)
        serializer.is_valid(raise_exception=True)

        address = serializer.data['address']
        client = DevinoClient(settings.DEVINO_LOGIN, settings.DEVINO_PASSWORD)
        devino_request = models.DevinoRequest.objects.create(api=consts.ADD_ADDRESS_SENDER,
                                                             data=json.dumps(serializer.data))
        try:
            answer = client.add_address_sender(address)
            models.DevinoAnswer.objects.create(
                code=answer.code,
                description=answer.description,
                result=answer.result,
                request=devino_request
            )
            return Response(answer.result)
        except DevinoException as ex:
            error_serializer = serializers.DevinoError.register_exception(devino_request, ex)
            return Response(error_serializer.data, status=status.HTTP_400_BAD_REQUEST)


class DelAddressSender(views.APIView):
    def delete(self, request):
        serializer = serializers.AddressSender(data=request.data)
        serializer.is_valid(raise_exception=True)

        address = serializer.data['address']
        client = DevinoClient(settings.DEVINO_LOGIN, settings.DEVINO_PASSWORD)
        devino_request = models.DevinoRequest.objects.create(api=consts.ADD_ADDRESS_SENDER,
                                                             data=json.dumps(serializer.data))
        try:
            answer = client.del_address_sender(address)
            models.DevinoAnswer.objects.create(
                code=answer.code,
                description=answer.description,
                result=answer.result,
                request=devino_request,
            )
            return Response(answer.result)
        except DevinoException as ex:
            error_serializer = serializers.DevinoError.register_exception(devino_request, ex)
            return Response(error_serializer.data, status=status.HTTP_400_BAD_REQUEST)


class GetTasks(views.APIView):
    def get(self, request):
        serializer = serializers.GetTasks(data=request.query_params)
        serializer.is_valid(raise_exception=True)

        range_start = serializer.validated_data['range_start']
        range_end = serializer.validated_data['range_end']
        client = DevinoClient(settings.DEVINO_LOGIN, settings.DEVINO_PASSWORD)
        devino_request = models.DevinoRequest.objects.create(api=consts.ADD_ADDRESS_SENDER,
                                                             data=json.dumps(serializer.data))
        try:
            answer = client.get_tasks(range_start, range_end)
            models.DevinoAnswer.objects.create(
                code=answer.code,
                description=answer.description,
                result=answer.result,
                request=devino_request,
            )
            return Response(answer.result)
        except DevinoException as ex:
            error_serializer = serializers.DevinoError.register_exception(devino_request, ex)
            return Response(error_serializer.data, status=status.HTTP_400_BAD_REQUEST)


class GetTask(views.APIView):
    def get(self, request):
        serializer = serializers.GetTask(data=request.query_params)
        serializer.is_valid(raise_exception=True)

        id_task = serializer.data['id_task']
        client = DevinoClient(settings.DEVINO_LOGIN, settings.DEVINO_PASSWORD)
        devino_request = models.DevinoRequest.objects.create(api=consts.ADD_ADDRESS_SENDER,
                                                             data=json.dumps(serializer.data))
        try:
            answer = client.get_task(id_task)
            models.DevinoAnswer.objects.create(
                code=answer.code,
                description=answer.description,
                result=answer.result,
                request=devino_request,
            )
            return Response(answer.result)
        except DevinoException as ex:
            error_serializer = serializers.DevinoError.register_exception(devino_request, ex)
            return Response(error_serializer.data, status=status.HTTP_400_BAD_REQUEST)


class AddTask(views.APIView):
    def post(self, request):
        serializer = serializers.AddTask(data=request.data)
        serializer.is_valid(raise_exception=True)

        name = serializer.data['name']
        sender_email = serializer.data['sender_address']
        sender_name = serializer.data['sender_name']
        subject = serializer.data['subject']
        text = serializer.data['text']
        type_task = serializer.data['type_task']
        start = serializer.data['start']
        end = serializer.data['end']
        user_id = serializer.data['user_id']
        contact_list = serializer.data['contact_list']
        template_id = serializer.data['template_id']
        duplicates = serializer.data['duplicates']

        client = DevinoClient(settings.DEVINO_LOGIN, settings.DEVINO_PASSWORD)
        devino_request = models.DevinoRequest.objects.create(api=consts.ADD_ADDRESS_SENDER,
                                                             data=json.dumps(serializer.data))
        try:
            answer = client.add_task(name, sender_email, sender_name, subject, text, type_task, start, end, user_id,
                                     contact_list, template_id, duplicates)
            models.DevinoAnswer.objects.create(
                code=answer.code,
                description=answer.description,
                result=answer.result,
                request=devino_request,
            )
            return Response(answer.result)
        except DevinoException as ex:
            error_serializer = serializers.DevinoError.register_exception(devino_request, ex)
            return Response(error_serializer.data, status=status.HTTP_400_BAD_REQUEST)


class EditTask(views.APIView):
    def put(self, request):
        serializer = serializers.EditTask(data=request.data)
        serializer.is_valid(raise_exception=True)

        id_task = serializer.data['id_task']
        name = serializer.data['name']
        sender_email = serializer.data['sender_address']
        sender_name = serializer.data['sender_name']
        subject = serializer.data['subject']
        text = serializer.data['text']
        type_task = serializer.data['type_task']
        start = serializer.data['start']
        end = serializer.data['end']
        user_id = serializer.data['user_id']
        contact_list = serializer.data['contact_list']
        template_id = serializer.data['template_id']
        duplicates = serializer.data['duplicates']

        client = DevinoClient(settings.DEVINO_LOGIN, settings.DEVINO_PASSWORD)
        devino_request = models.DevinoRequest.objects.create(api=consts.ADD_ADDRESS_SENDER,
                                                             data=json.dumps(serializer.data))
        try:
            answer = client.edit_task(id_task, name, sender_email, sender_name, subject, text, type_task, start, end,
                                      user_id, contact_list, template_id, duplicates)
            models.DevinoAnswer.objects.create(
                code=answer.code,
                description=answer.description,
                result=answer.result,
                request=devino_request,
            )
            return Response(answer.result)
        except DevinoException as ex:
            error_serializer = serializers.DevinoError.register_exception(devino_request, ex)
            return Response(error_serializer.data, status=status.HTTP_400_BAD_REQUEST)


class EditTaskStatus(views.APIView):
    def put(self, request):
        serializer = serializers.EditTaskStatus(data=request.data)
        serializer.is_valid(raise_exception=True)

        id_task = serializer.data['id_task']
        state = serializer.data['state']
        client = DevinoClient(settings.DEVINO_LOGIN, settings.DEVINO_PASSWORD)
        devino_request = models.DevinoRequest.objects.create(api=consts.ADD_ADDRESS_SENDER,
                                                             data=json.dumps(serializer.data))
        try:
            answer = client.edit_task_status(id_task, state)
            models.DevinoAnswer.objects.create(
                code=answer.code,
                description=answer.description,
                result=answer.result,
                request=devino_request,
            )
            return Response(answer.result)
        except DevinoException as ex:
            error_serializer = serializers.DevinoError.register_exception(devino_request, ex)
            return Response(error_serializer.data, status=status.HTTP_400_BAD_REQUEST)


class GetTemplate(views.APIView):
    def get(self, request):
        serializer = serializers.GetTemplate(data=request.query_params)
        serializer.is_valid(raise_exception=True)

        id_template = serializer.data['id_template']
        client = DevinoClient(settings.DEVINO_LOGIN, settings.DEVINO_PASSWORD)
        devino_request = models.DevinoRequest.objects.create(api=consts.ADD_ADDRESS_SENDER,
                                                             data=json.dumps(serializer.data))
        try:
            answer = client.get_template(id_template)
            models.DevinoAnswer.objects.create(
                code=answer.code,
                description=answer.description,
                result=answer.result,
                request=devino_request,
            )
            return Response(answer.result)
        except DevinoException as ex:
            error_serializer = serializers.DevinoError.register_exception(devino_request, ex)
            return Response(error_serializer.data, status=status.HTTP_400_BAD_REQUEST)


class AddTemplate(views.APIView):
    def post(self, request):
        serializer = serializers.AddTemplate(data=request.data)
        serializer.is_valid(raise_exception=True)

        name = serializer.data['name']
        text = serializer.data['text']
        sender_email = serializer.data['sender_email']
        sender_name = serializer.data['sender_name']
        subject = serializer.data['subject']
        user_template_id = serializer.data['user_template_id']

        client = DevinoClient(settings.DEVINO_LOGIN, settings.DEVINO_PASSWORD)
        devino_request = models.DevinoRequest.objects.create(api=consts.ADD_ADDRESS_SENDER,
                                                             data=json.dumps(serializer.data))
        try:
            answer = client.add_template(name, text, sender_email, sender_name, subject, user_template_id)
            models.DevinoAnswer.objects.create(
                code=answer.code,
                description=answer.description,
                result=answer.result,
                request=devino_request,
            )
            return Response(answer.result)
        except DevinoException as ex:
            error_serializer = serializers.DevinoError.register_exception(devino_request, ex)
            return Response(error_serializer.data, status=status.HTTP_400_BAD_REQUEST)


class EditTemplate(views.APIView):
    def put(self, request):
        serializer = serializers.EditTemplate(data=request.data)
        serializer.is_valid(raise_exception=True)

        id_template = serializer.data['id_template']
        name = serializer.data['name']
        text = serializer.data['text']
        sender_email = serializer.data['sender_email']
        sender_name = serializer.data['sender_name']
        subject = serializer.data['subject']
        user_template_id = serializer.data['user_template_id']

        client = DevinoClient(settings.DEVINO_LOGIN, settings.DEVINO_PASSWORD)
        devino_request = models.DevinoRequest.objects.create(api=consts.ADD_ADDRESS_SENDER,
                                                             data=json.dumps(serializer.data))
        try:
            answer = client.edit_template(id_template, name, text, sender_email, sender_name, subject, user_template_id)
            models.DevinoAnswer.objects.create(
                code=answer.code,
                description=answer.description,
                result=answer.result,
                request=devino_request,
            )
            return Response(answer.result)
        except DevinoException as ex:
            error_serializer = serializers.DevinoError.register_exception(devino_request, ex)
            return Response(error_serializer.data, status=status.HTTP_400_BAD_REQUEST)


class DelTemplate(views.APIView):
    def delete(self, request):
        serializer = serializers.DelTemplate(data=request.data)
        serializer.is_valid(raise_exception=True)

        id_template = serializer.data['id_template']
        client = DevinoClient(settings.DEVINO_LOGIN, settings.DEVINO_PASSWORD)
        devino_request = models.DevinoRequest.objects.create(api=consts.ADD_ADDRESS_SENDER,
                                                             data=json.dumps(serializer.data))
        try:
            answer = client.del_template(id_template)
            models.DevinoAnswer.objects.create(
                code=answer.code,
                description=answer.description,
                result=answer.result,
                request=devino_request,
            )
            return Response(answer.result)
        except DevinoException as ex:
            error_serializer = serializers.DevinoError.register_exception(devino_request, ex)
            return Response(error_serializer.data, status=status.HTTP_400_BAD_REQUEST)


class GetState(views.APIView):
    def get(self, request):
        serializer = serializers.GetState(data=request.query_params)
        serializer.is_valid(raise_exception=True)

        id_template = serializer.data['id_template']
        start = serializer.data['start']
        end = serializer.data['end']

        client = DevinoClient(settings.DEVINO_LOGIN, settings.DEVINO_PASSWORD)
        devino_request = models.DevinoRequest.objects.create(api=consts.ADD_ADDRESS_SENDER,
                                                             data=json.dumps(serializer.data))
        try:
            answer = client.get_state(id_template, start, end)
            models.DevinoAnswer.objects.create(
                code=answer.code,
                description=answer.description,
                result=answer.result,
                request=devino_request,
            )
            return Response(answer.result)
        except DevinoException as ex:
            error_serializer = serializers.DevinoError.register_exception(devino_request, ex)
            return Response(error_serializer.data, status=status.HTTP_400_BAD_REQUEST)


class GetStateDetailing(views.APIView):
    def get(self, request):
        serializer = serializers.GetStateDetailing(data=request.query_params)
        serializer.is_valid(raise_exception=True)

        id_template = serializer.data['id_template']
        start = serializer.data['start']
        end = serializer.data['end']
        state = serializer.data['state']
        range_start = serializer.data['range_start']
        range_end = serializer.data['range_end']

        client = DevinoClient(settings.DEVINO_LOGIN, settings.DEVINO_PASSWORD)
        devino_request = models.DevinoRequest.objects.create(api=consts.ADD_ADDRESS_SENDER,
                                                             data=json.dumps(serializer.data))
        try:
            answer = client.get_state_detailing(id_template, start, end, state, range_start, range_end)
            models.DevinoAnswer.objects.create(
                code=answer.code,
                description=answer.description,
                result=answer.result,
                request=devino_request,
            )
            return Response(answer.result)
        except DevinoException as ex:
            error_serializer = serializers.DevinoError.register_exception(devino_request, ex)
            return Response(error_serializer.data, status=status.HTTP_400_BAD_REQUEST)


class SendMessage(views.APIView):
    def post(self, request):
        serializer = serializers.SendMessage(data=request.data)
        serializer.is_valid(raise_exception=True)

        sender_address = serializer.data['sender_address']
        sender_name = serializer.data['sender_name']
        recipient_address = serializer.data['recipient_address']
        recipient_name = serializer.data['recipient_name']
        subject = serializer.data['subject']
        text = serializer.data['text']
        user_message_id = serializer.data['user_message_id']
        user_campaign_id = serializer.data['user_campaign_id']
        template_id = serializer.data['template_id']

        client = DevinoClient(settings.DEVINO_LOGIN, settings.DEVINO_PASSWORD)
        devino_request = models.DevinoRequest.objects.create(api=consts.ADD_ADDRESS_SENDER,
                                                             data=json.dumps(serializer.data))
        try:
            answer = client.send_transactional_message(sender_address, sender_name, recipient_address, recipient_name,
                                                       subject, text, user_message_id, user_campaign_id, template_id)
            models.DevinoAnswer.objects.create(
                code=answer.code,
                description=answer.description,
                result=answer.result,
                request=devino_request,
            )
            return Response(answer.result)
        except DevinoException as ex:
            error_serializer = serializers.DevinoError.register_exception(devino_request, ex)
            return Response(error_serializer.data, status=status.HTTP_400_BAD_REQUEST)


class GetStatusMessages(views.APIView):
    def get(self, request):
        serializer = serializers.GetStatusMessages(data=request.query_params)
        serializer.is_valid(raise_exception=True)

        id_messages = serializer.data['id_messages']
        client = DevinoClient(settings.DEVINO_LOGIN, settings.DEVINO_PASSWORD)
        devino_request = models.DevinoRequest.objects.create(api=consts.ADD_ADDRESS_SENDER,
                                                             data=json.dumps(serializer.data))
        try:
            answer = client.get_status_transactional_message(id_messages)
            models.DevinoAnswer.objects.create(
                code=answer.code,
                description=answer.description,
                result=answer.result,
                request=devino_request,
            )
            return Response(answer.result)
        except DevinoException as ex:
            error_serializer = serializers.DevinoError.register_exception(devino_request, ex)
            return Response(error_serializer.data, status=status.HTTP_400_BAD_REQUEST)
