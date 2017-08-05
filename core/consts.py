GET_SENDER_ADDRESSES = 'get_addresses_sender'
ADD_SENDER_ADDRESS = 'add_address_sender'
DEL_SENDER_ADDRESS = 'del_address_sender'
GET_TASKS_LIST = 'get_bulk_list'
GET_TASK = 'get_bulk'
ADD_TASK = 'add_bulk'
EDIT_TASK = 'edit_bulk'
EDIT_TASK_STATUS = 'edit_bulk_status'
GET_TEMPLATE = 'get_template'
ADD_TEMPLATE = 'add_template'
EDIT_TEMPLATE = 'edit_template'
DEL_TEMPLATE = 'del_template'
GET_STATE = 'get_state'
GET_STATE_DETAILING = 'get_state_detailing'
SEND_MESSAGE = 'send_message'
GET_STATUS_MESSAGE = 'get_status_message'

API = [GET_SENDER_ADDRESSES, ADD_SENDER_ADDRESS, DEL_SENDER_ADDRESS, GET_TASKS_LIST, GET_TASK, ADD_TASK, EDIT_TASK,
       EDIT_TASK_STATUS, GET_TEMPLATE, ADD_TEMPLATE, EDIT_TEMPLATE, DEL_TEMPLATE, GET_STATE, GET_STATE_DETAILING,
       SEND_MESSAGE, GET_STATUS_MESSAGE]
API_CHOICES = [(status, status) for status in API]

STATUS_OK = 'ok'
STATUS_BAD_REQUEST = 'validation_error'
STATUS_ERROR_API = 'internal_error'
