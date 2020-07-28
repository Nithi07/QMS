from django import forms
from QMS.models import ListAuditors
from QMS.models import EmployeeDetails
from django.urls import reverse
from crispy_forms.bootstrap import Field, InlineRadios, TabHolder, Tab,FormActions
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout, Div, Fieldset,Reset,Button,HTML,ButtonHolder


class Auditorlistform(forms.ModelForm):

    auditors = forms.ModelChoiceField(queryset=EmployeeDetails.objects.all(),empty_label='Select')


    def __init__(self, *args, **kwargs):
        super(Auditorlistform, self).__init__(*args, **kwargs)
        self.fields['auditors'].label_from_instance = lambda obj: "%s" % obj.emp_name
        self.fields['auditors'].widget.attrs['style'] = 'height:30px;'
        self.helper = FormHelper()
        self.helper.form_class = 'form-horizontal'
        self.helper.layout = Layout(Field(
            'auditors'),
            ButtonHolder(
                Submit('submit', 'Submit', css_class='btn-success'),
                HTML("""<a class= "btn btn-success" href= "{% url 'QMS:auditorlistview' %}"> Back</a>""")
            )
            )

    class Meta:
        model = ListAuditors
        fields = ['auditors']
