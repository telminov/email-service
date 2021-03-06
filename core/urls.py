from django.conf.urls import url

from rest_framework_swagger.views import get_swagger_view

from .views import rest, ui

urlpatterns = [
    url(r'^docs/$', get_swagger_view(title='API')),

    url(r'^api/get_sender_addresses/$', rest.GetSenderAddresses.as_view(), name='get_sender_addresses'),
    url(r'^api/add_sender_address/$', rest.AddSenderAddress.as_view(), name='add_sender_address'),
    url(r'^api/del_sender_address/$', rest.DelSenderAddress.as_view(), name='del_sender_address'),
    url(r'^api/get_tasks/$', rest.GetTasks.as_view(), name='get_tasks'),
    url(r'^api/get_task/$', rest.GetTask.as_view(), name='get_task'),
    url(r'^api/add_task/$', rest.AddTask.as_view(), name='add_task'),
    url(r'^api/edit_task/$', rest.EditTask.as_view(), name='edit_task'),
    url(r'^api/edit_task_status/$', rest.EditTaskStatus.as_view(), name='edit_task_status'),
    url(r'^api/get_template/$', rest.GetTemplate.as_view(), name='get_template'),
    url(r'^api/add_template/$', rest.AddTemplate.as_view(), name='add_template'),
    url(r'^api/edit_template/$', rest.EditTemplate.as_view(), name='edit_template'),
    url(r'^api/del_template/$', rest.DelTemplate.as_view(), name='del_template'),
    url(r'^api/get_state/$', rest.GetState.as_view(), name='get_state'),
    url(r'^api/get_state_detailing/$', rest.GetStateDetailing.as_view(), name='get_state_detailing'),
    url(r'^api/send_message/$', rest.SendMessage.as_view(), name='send_message'),
    url(r'^api/get_status_messages/$', rest.GetStatusMessages.as_view(), name='get_status_messages'),

    url(r'^$', ui.Index.as_view()),
    url(r'^send_message/$', ui.SendMessage.as_view(), name='send_message_interface'),
]
