# email-service
Microservice django-project for [sw-python-email-devino](https://github.com/telminov/sw-python-email-devino) library.

## Example send bulk

### Service authentication
Session authentication or token authentication (http://www.django-rest-framework.org/api-guide/authentication/#tokenauthentication)

### Add sender address in Devino.
After adding the sender's address, you need to contact the Devino manager to confirm the address

```python
import requests
data = {
    'address': 'sender_address@test.test'
}
requests.post('http://127.0.0.1:8000/api/add_address_sender/', json=data, headers={'Authorization': 'Token ...'})
```

### Get exists addresses
```python
import requests
response = requests.get('http://127.0.0.1:8000/api/get_addresses_sender/',
                        headers={'Authorization': 'Token ...'})
response.json()
{'code': 'ok',
 'description': 'ok',
 'result': [{'Confirmed': True, 'SenderAddress': 'sender_address@test.test'}]}


```

### Send one message to email

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

response = requests.post('http://127.0.0.1:8000/api/send_message/', json=data, headers={'Authorization': 'Token ...'})
response.json()
```

### Send message to exists contacts

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

requests.post('http://127.0.0.1:8000/api/add_task/', json=data, headers={'Authorization': 'Token ...'})
```
