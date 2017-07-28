# email-service
Microservice django-project for [sw-python-email-devino](https://github.com/telminov/sw-python-email-devino) library.

## Example send bulk

1. Add sender address in Devino
 
2. Add contact group in Devino 

3. Send request

```python
import requests

data = {
    'name': 'Test name', 
    'sender_email': 'sender_address@test.test', 
    'sender_name': 'Other test name', 
    'subject': 'Test subj', 
    'text': 'Test text', 
    'start': '07/15/2100 16:00', 
    'contact_list': [[559446, True]],   # id contact group and boolean value include or not include a group in the bulk
}

requests.post('http://127.0.0.1:8000/api/add_task/', json=data)
```

## Example send one message

1. Add sender addresses in Devino

2. Send request

```python
import requests

data = {
    'recipient_email': 'recipient_address@test.test',
    'recipient_name': 'Test name',
    'sender_email': 'sender_address@test.test', 
    'sender_name': 'Other test name', 
    'subject': 'Test subj', 
    'text': 'Test text', 
}

requests.post('http://127.0.0.1:8000/api/send_message/', json=data)
```