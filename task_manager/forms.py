from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from task_manager.models import Worker


class WorkerCreationForm(UserCreationForm):
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)

    class Meta(UserCreationForm.Meta):
        model = Worker
        fields = UserCreationForm.Meta.fields + ("first_name", "last_name", "position", )


class WorkerUpdateForm(UserChangeForm):
    password = None

    class Meta:
        model = get_user_model()
        fields = ("first_name", "last_name", "position", )