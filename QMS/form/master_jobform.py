from django import forms
from QMS.models import JobType
from QMS.models import ClientName
from QMS.models import EndUser
from QMS.models import JobDetails
from django.urls import reverse
from crispy_forms.bootstrap import Field, InlineRadios, TabHolder, Tab
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout, Div, Fieldset


class JobTypeform(forms.ModelForm):
    j_type = forms.CharField(max_length=25)

    def __init__(self, *args, **kwargs):
        super(JobTypeform, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.add_input(Submit('submit', 'Submit', css_class='btn-success'))
        self.helper.form_class = 'form-horizontal'
        self.helper.layout = Layout(
            'j_type',
        )

    class Meta:
        model = JobType
        fields = ['j_type']


class ClientNameform(forms.ModelForm):
    c_name = forms.CharField(max_length=25)

    def __init__(self, *args, **kwargs):
        super(ClientNameform, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.add_input(Submit('submit', 'Submit', css_class='btn-success'))
        self.helper.form_class = 'form-horizontal'
        self.helper.layout = Layout(
            'c_name',
        )

    class Meta:
        model = ClientName
        fields = ['c_name']


class EndUserform(forms.ModelForm):
    e_user = forms.CharField(max_length=25)

    def __init__(self, *args, **kwargs):
        super(EndUserform, self).__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.add_input(Submit('submit', 'Submit', css_class='btn-success'))
        self.helper.form_class = 'form-horizontal'
        self.helper.layout = Layout(
            'e_user',
        )

    class Meta:
        model = EndUser
        fields = ['e_user']
