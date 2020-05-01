from django.forms import ModelForm
from guardian.shortcuts import get_objects_for_user
from . import models


class StreamFilteredApplicationForm(ModelForm):
    class Meta:
        model = models.Stream
        fields = ['name', 'application']

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

        # limit the stream selection to user-accessible streams
        self.fields['application'].queryset = get_objects_for_user(user, 'rtmp.view_application')
