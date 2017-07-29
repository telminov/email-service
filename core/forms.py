from django import forms


class AddTask(forms.Form):
    name = forms.CharField()
    sender_email = forms.EmailField()
    sender_name = forms.CharField()
    subject = forms.CharField()
    text = forms.CharField()
    type_task = forms.IntegerField(required=False)
    start = forms.DateTimeField(required=False)
    end = forms.DateTimeField(required=False)
    user_id = forms.CharField(required=False)
    template_id = forms.CharField(required=False)
    duplicates = forms.NullBooleanField(required=False)


class ContactList(forms.Form):
    id = forms.IntegerField()
    included = forms.BooleanField()
