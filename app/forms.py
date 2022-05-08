from django.contrib.auth.forms import AuthenticationForm
from django.forms import CharField, Form, ModelForm, TextInput, PasswordInput

from app.models import Git


class GitModelForm(ModelForm):
    class Meta:
        model = Git
        fields = ('username', 'password',)
        widgets = {
            'password': TextInput(attrs={'type': 'password'})
        }


class LoginUserForm(AuthenticationForm):
    username = CharField(label='Login')
    password = CharField(label='Password', widget=PasswordInput)
