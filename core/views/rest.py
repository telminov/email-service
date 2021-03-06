import json

from django.conf import settings
from rest_framework import views
from rest_framework.response import Response
from rest_framework import status

from email_devino.client import DevinoClient
from email_devino.client import DevinoException

from core import models
from core import consts
from core import serializers
from core.utils import date_handler


class BaseDevino(views.APIView):
    api_resource = None
    serializer = None
    api_resource_lib = None

    def devino_request(self, serializer=None):
        if serializer:
            serializer.is_valid(raise_exception=True)

        json_data = json.dumps(
            serializer.validated_data if serializer else None,
            default=date_handler
        )
        devino_request = models.DevinoRequest.objects.create(api_resource=self.api_resource, data=json_data)

        try:
            if serializer:
                answer = self.api_resource_lib(**serializer.validated_data)
            else:
                answer = self.api_resource_lib()

            models.DevinoAnswer.objects.create(
                code=answer.code,
                description=answer.description,
                result=answer.result,
                request=devino_request,
            )
            if answer.code == consts.STATUS_BAD_REQUEST:
                status_response = status.HTTP_400_BAD_REQUEST
            elif answer.code == consts.STATUS_ERROR_API:
                status_response = status.HTTP_500_INTERNAL_SERVER_ERROR
            else:
                status_response = status.HTTP_200_OK
            return Response({'code': answer.code, 'description': answer.description, 'result': answer.result},
                            status=status_response)

        except DevinoException as ex:
            error = models.DevinoAnswer.objects.create(
                code=ex.error.code,
                description=ex.error.description,
                request=devino_request,
                is_fail=True,
            )
            return Response({'code': error.code, 'description': error.description}, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        serializer = self.serializer
        if serializer:
            serializer = serializer(data=request.query_params)
        response = self.devino_request(serializer)
        return response

    def post(self, request):
        serializer = self.serializer
        if serializer:
            serializer = serializer(data=request.data)
        response = self.devino_request(serializer)
        return response

    def put(self, request):
        serializer = self.serializer
        if serializer:
            serializer = serializer(data=request.data)
        response = self.devino_request(serializer)
        return response

    def delete(self, request):
        serializer = self.serializer
        if serializer:
            serializer = serializer(data=request.data)
        response = self.devino_request(serializer)
        return response


class GetSenderAddresses(BaseDevino):
    api_resource = consts.GET_SENDER_ADDRESSES
    api_resource_lib = DevinoClient(settings.DEVINO_LOGIN, settings.DEVINO_PASSWORD).get_sender_addresses
    http_method_names = ['get', ]


class AddSenderAddress(BaseDevino):
    api_resource = consts.ADD_SENDER_ADDRESS
    serializer = serializers.SenderAddress
    api_resource_lib = DevinoClient(settings.DEVINO_LOGIN, settings.DEVINO_PASSWORD).add_sender_address
    http_method_names = ['post', ]


class DelSenderAddress(BaseDevino):
    api_resource = consts.DEL_SENDER_ADDRESS
    serializer = serializers.SenderAddress
    api_resource_lib = DevinoClient(settings.DEVINO_LOGIN, settings.DEVINO_PASSWORD).del_sender_address
    http_method_names = ['delete', ]


class GetTasks(BaseDevino):
    api_resource = consts.GET_TASKS_LIST
    serializer = serializers.GetTasks
    api_resource_lib = DevinoClient(settings.DEVINO_LOGIN, settings.DEVINO_PASSWORD).get_tasks
    http_method_names = ['get', ]


class GetTask(BaseDevino):
    api_resource = consts.GET_TASK
    serializer = serializers.GetTask
    api_resource_lib = DevinoClient(settings.DEVINO_LOGIN, settings.DEVINO_PASSWORD).get_task
    http_method_names = ['get', ]


class AddTask(BaseDevino):
    api_resource = consts.ADD_TASK
    serializer = serializers.AddTask
    api_resource_lib = DevinoClient(settings.DEVINO_LOGIN, settings.DEVINO_PASSWORD).add_task
    http_method_names = ['post', ]


class EditTask(BaseDevino):
    api_resource = consts.EDIT_TASK
    serializer = serializers.EditTask
    api_resource_lib = DevinoClient(settings.DEVINO_LOGIN, settings.DEVINO_PASSWORD).edit_task
    http_method_names = ['put', ]


class EditTaskStatus(BaseDevino):
    api_resource = consts.EDIT_TASK_STATUS
    serializer = serializers.EditTaskStatus
    api_resource_lib = DevinoClient(settings.DEVINO_LOGIN, settings.DEVINO_PASSWORD).edit_task_status
    http_method_names = ['put', ]


class GetTemplate(BaseDevino):
    api_resource = consts.GET_TEMPLATE
    serializer = serializers.GetTemplate
    api_resource_lib = DevinoClient(settings.DEVINO_LOGIN, settings.DEVINO_PASSWORD).get_template
    http_method_names = ['get', ]


class AddTemplate(BaseDevino):
    api_resource = consts.ADD_TEMPLATE
    serializer = serializers.AddTemplate
    api_resource_lib = DevinoClient(settings.DEVINO_LOGIN, settings.DEVINO_PASSWORD).add_template
    http_method_names = ['post', ]


class EditTemplate(BaseDevino):
    api_resource = consts.EDIT_TEMPLATE
    serializer = serializers.EditTemplate
    api_resource_lib = DevinoClient(settings.DEVINO_LOGIN, settings.DEVINO_PASSWORD).edit_template
    http_method_names = ['put', ]


class DelTemplate(BaseDevino):
    api_resource = consts.DEL_TEMPLATE
    serializer = serializers.DelTemplate
    api_resource_lib = DevinoClient(settings.DEVINO_LOGIN, settings.DEVINO_PASSWORD).del_template
    http_method_names = ['delete', ]


class GetState(BaseDevino):
    api_resource = consts.GET_STATE
    serializer = serializers.GetState
    api_resource_lib = DevinoClient(settings.DEVINO_LOGIN, settings.DEVINO_PASSWORD).get_state
    http_method_names = ['get', ]


class GetStateDetailing(BaseDevino):
    api_resource = consts.GET_STATE_DETAILING
    serializer = serializers.GetStateDetailing
    api_resource_lib = DevinoClient(settings.DEVINO_LOGIN, settings.DEVINO_PASSWORD).get_state_detailing
    http_method_names = ['get', ]


class SendMessage(BaseDevino):
    api_resource = consts.SEND_MESSAGE
    serializer = serializers.SendMessage
    api_resource_lib = DevinoClient(settings.DEVINO_LOGIN, settings.DEVINO_PASSWORD).send_transactional_message
    http_method_names = ['post', ]


class GetStatusMessages(BaseDevino):
    api_resource = consts.GET_STATUS_MESSAGE
    serializer = serializers.GetStatusMessages
    api_resource_lib = DevinoClient(settings.DEVINO_LOGIN, settings.DEVINO_PASSWORD).get_status_transactional_message
    http_method_names = ['get', ]
