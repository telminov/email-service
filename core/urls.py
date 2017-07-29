from django.conf.urls import url

from . import views

urlpatterns = [
    # url(r'^$', views.Index.as_view()),
    url(r'^api/get_addresses_sender/$', views.GetAddressesSender.as_view(), name='get_addresses_sender'),
    url(r'^api/add_address_sender/$', views.AddAddressSender.as_view(), name='add_address_sender'),
    url(r'^api/del_address_sender/$', views.DelAddressSender.as_view(), name='del_address_sender'),
    url(r'^api/get_tasks/$', views.GetTasks.as_view(), name='get_tasks'),
    url(r'^api/get_task/$', views.GetTask.as_view(), name='get_task'),
    url(r'^api/add_task/$', views.AddTask.as_view(), name='add_task'),
    url(r'^api/edit_task/$', views.EditTask.as_view(), name='edit_task'),
    url(r'^api/edit_task_status/$', views.EditTaskStatus.as_view(), name='edit_task_status'),
    url(r'^api/get_template/$', views.GetTemplate.as_view(), name='get_template'),
    url(r'^api/add_template/$', views.AddTemplate.as_view(), name='add_template'),
    url(r'^api/edit_template/$', views.EditTemplate.as_view(), name='edit_template'),
    url(r'^api/del_template/$', views.DelTemplate.as_view(), name='del_template'),
    url(r'^api/get_state/$', views.GetState.as_view(), name='get_state'),
    url(r'^api/get_state_detailing/$', views.GetStateDetailing.as_view(), name='get_state_detailing'),
    url(r'^api/send_message/$', views.SendMessage.as_view(), name='send_message'),
    url(r'^api/get_status_messages/$', views.GetStatusMessages.as_view(), name='get_status_messages'),
]
