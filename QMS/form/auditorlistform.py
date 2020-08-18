from django import forms
from QMS.models import ListAuditors
from QMS.models import EmployeeDetails
from django.urls import reverse
from crispy_forms.bootstrap import Field, InlineRadios, TabHolder, Tab,FormActions
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout, Div, Fieldset,Reset,Button,HTML,ButtonHolder


class Auditorlistform(forms.ModelForm):

    auditors = forms.ModelMultipleChoiceField(widget=forms.CheckboxSelectMultiple(),queryset=EmployeeDetails.objects.filter(emp_status=0))

    def __init__(self, *args, **kwargs):
        super(Auditorlistform, self).__init__(*args, **kwargs)
        lis = []
        for i in ListAuditors.objects.all():
            try:
                lis.append(i.auditors.id)
            except:
                pass
        self.fields['auditors'].queryset = EmployeeDetails.objects.filter(emp_status=0).exclude(id__in=lis)
        self.fields['auditors'].label_from_instance = lambda obj: "%s" % obj.emp_name
        self.helper = FormHelper()
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-lg-2'
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
