from django.conf.urls import url

from .views import rest, views

urlpatterns = [
    # url(r'^$', views.Index.as_view()),
    url(r'^api/get_addresses_sender/$', rest.GetAddressesSender.as_view(), name='get_addresses_sender'),
    url(r'^api/add_address_sender/$', rest.AddAddressSender.as_view(), name='add_address_sender'),
    url(r'^api/del_address_sender/$', rest.DelAddressSender.as_view(), name='del_address_sender'),
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

    url(r'^send_message/$', views.SendMessage.as_view(), name='send_message_interface'),
]
