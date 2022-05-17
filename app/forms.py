import os

from django.contrib.auth.forms import AuthenticationForm
from django.core.exceptions import ValidationError
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


class SudoEnterForm(Form):
    sudo_key = CharField(label='Sudo key', widget=PasswordInput)

    def clean_sudo_key(self):
        sudo_key = self.cleaned_data.get('sudo_key')
        if sudo_key != os.environ['secret_key']:
            raise ValidationError('Invalid sudo key')

        return sudo_key