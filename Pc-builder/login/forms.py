from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Client
from collections import OrderedDict


class RegistrationForm(UserCreationForm):
    email = forms.EmailField(max_length=100, help_text='Required', required=True)
    first_name = forms.CharField(max_length=50)
    last_name = forms.CharField(max_length=50)
    phone_number = forms.CharField(max_length=25)
    address = forms.CharField(max_length=100)
    birthday = forms.DateField()

    class Meta:
        model = Client
        fields = {
            'username', 
            'email', 
            'first_name', 
            'last_name', 
            'address', 
            'birthday', 
            'phone_number', 
            'password1', 
            'password2', }
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields = OrderedDict(
            (field_name, self.fields[field_name])
            for field_name in [
                'username', 'email', 'first_name', 'last_name','address', 'birthday',
                'phone_number', 'password1', 'password2'
            ]
        )
        
    def save(self, commit: bool):
        user = super(RegistrationForm, self).save(commit=False)

        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.address = self.cleaned_data['address']
        user.birthday = self.cleaned_data['birthday']
        user.phone_number = self.cleaned_data['phone_number']

        if commit:
            user.save(True)

        return user

