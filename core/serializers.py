from rest_framework import serializers

from . import models


class DevinoError(serializers.ModelSerializer):

    class Meta:
        model = models.DevinoError
        fields = ('code', 'description', 'request')

    @classmethod
    def register_exception(cls, devino_request, ex):
        data = {
            'request': devino_request.pk,
        }
        if ex.error:
            data['code'] = ex.error.code
            data['description'] = ex.error.description

        serializer = cls(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return serializer


class AddressSender(serializers.Serializer):
    address = serializers.EmailField()


class GetTasks(serializers.Serializer):
    range_start = serializers.IntegerField(default=1)
    range_end = serializers.IntegerField(default=100)


class GetTask(serializers.Serializer):
    id_task = serializers.IntegerField()


class AddTask(serializers.Serializer):
    name = serializers.CharField()
    sender_address = serializers.EmailField()
    sender_name = serializers.CharField()
    subject = serializers.CharField()
    text = serializers.CharField()
    type_task = serializers.IntegerField(default=1)
    start = serializers.DateTimeField(default=None)
    end = serializers.DateTimeField(default=None)
    user_id = serializers.CharField(default="")
    contact_list = serializers.ListField(child=serializers.ListField(min_length=2, max_length=2), default=None)
    template_id = serializers.CharField(default="")
    duplicates = serializers.NullBooleanField(default=None)


class EditTask(AddTask):
    id_task = serializers.IntegerField()


class EditTaskStatus(serializers.Serializer):
    id_task = serializers.IntegerField()
    state = serializers.CharField()


class GetTemplate(serializers.Serializer):
    id_template = serializers.IntegerField()


class AddTemplate(serializers.Serializer):
    name = serializers.CharField()
    text = serializers.CharField()
    sender_email = serializers.EmailField(default=None)
    sender_name = serializers.CharField(default=None)
    subject = serializers.CharField(default=None)
    user_template_id = serializers.CharField(default=None)


class EditTemplate(serializers.Serializer):
    id_template = serializers.IntegerField()
    name = serializers.CharField()
    text = serializers.CharField()
    sender_email = serializers.EmailField(default=None)
    sender_name = serializers.CharField(default=None)
    subject = serializers.CharField(default=None)
    user_template_id = serializers.CharField(default=None)


class DelTemplate(serializers.Serializer):
    id_template = serializers.IntegerField()


class GetState(serializers.Serializer):
    id_task = serializers.IntegerField()
    start = serializers.DateTimeField(default=None)
    end = serializers.DateTimeField(default=None)


class GetStateDetailing(serializers.Serializer):
    id_task = serializers.IntegerField()
    start = serializers.DateField(default=None)
    end = serializers.DateField(default=None)
    state = serializers.CharField(default=None)
    range_start = serializers.IntegerField(default=1)
    range_end = serializers.IntegerField(default=100)


class SendMessage(serializers.Serializer):
    sender_address = serializers.EmailField()
    sender_name = serializers.CharField()
    recipient_address = serializers.EmailField()
    recipient_name = serializers.CharField()
    subject = serializers.CharField()
    text = serializers.CharField()
    user_message_id = serializers.CharField(default=None)
    user_campaign_id = serializers.CharField(default=None)
    tempale_id = serializers.CharField(default=None)


class GetStatusMessages(serializers.Serializer):
    id_messages = serializers.ListField(child=serializers.CharField())
