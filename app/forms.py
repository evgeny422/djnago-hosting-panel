from django.forms import CharField, Form, ModelForm, TextInput

from app.models import Git


class GitModelForm(ModelForm):
    class Meta:
        model = Git
        fields = ('username', 'password',)
        widgets = {
            'password': TextInput(attrs={'type': 'password'})
        }
