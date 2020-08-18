from django import forms
from QMS import default_choices
from QMS.models import EmployeeDetails
from QMS.models import EmployeDepartment
from QMS.models import EmployePosition
from QMS.models import Project_Details,Teamwise
from django.urls import reverse
from Timesheet.settings import DATE_INPUT_FORMATS
from crispy_forms.bootstrap import Field, InlineRadios, TabHolder, Tab,FormActions
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout, Div, Fieldset,Reset,Button,HTML,ButtonHolder

class Project_Detailsform(forms.ModelForm):
    project_code = forms.CharField(max_length=15,label = 'Project Code')
    project_name = forms.CharField(max_length=300,label = 'Project Name')
    project_type = forms.ChoiceField(choices=default_choices.type,label = 'Type')
    project_start_date = forms.DateField(label = 'Start Date',required=True,input_formats=DATE_INPUT_FORMATS,widget=forms.DateInput(attrs={'id':'datetimepicker1'},format='%d-%m-%Y'))
    project_end_date = forms.DateField(label = 'End Date',required=True,input_formats=DATE_INPUT_FORMATS,widget=forms.DateInput(attrs={'id':'datetimepicker2'},format='%d-%m-%Y'))
    project_status = forms.ChoiceField(choices=default_choices.project_status,label = 'Status')

    def __init__(self, *args, **kwargs):
        super(Project_Detailsform, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.fields['project_type'].widget.attrs['style'] = 'height:40px;'
        self.fields['project_status'].widget.attrs['style'] = 'height:40px;'
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-lg-2'
        self.helper.layout = Layout(Field(
            'project_code',
            'project_name',
            'project_type',
            'project_start_date',
            'project_end_date',
            'project_status'),
            ButtonHolder(
                Submit('submit', 'Submit', css_class='btn-success'),
                Reset('reset','Reset', css_class='btn-success'),
                HTML("""<a class= "btn btn-success" href= "{% url 'QMS:projectview' %}"> Back</a>""")
            )
            )

    class Meta:
        model = Project_Details
        fields = ['project_code','project_name','project_type','project_start_date','project_end_date','project_status']


class Teamwiseform(forms.ModelForm):
    tw_project_code = forms.ModelChoiceField(queryset=Project_Details.objects.all(),empty_label = '---Select---',required=True,label = 'Project Code')
    sub_code = forms.CharField(max_length=20,label = 'Sub Code')
    m=EmployePosition.objects.get(emp_posn='Manager')
    manager = forms.ModelChoiceField(queryset=EmployeeDetails.objects.filter(emp_position=m),empty_label = '---Select---',required=True,label = 'Manager')
    department = forms.ModelChoiceField(queryset=EmployeDepartment.objects.all(),empty_label='--- Select ---',label = 'Department')
    team_manhours = forms.IntegerField()
    tl=EmployePosition.objects.get(emp_posn='Team Lead')
    list_of_auditee = forms.ModelChoiceField(queryset=EmployeeDetails.objects.filter(emp_position=tl),empty_label = '--- Select ---',label = 'Auditor')

    def __init__(self, *args, **kwargs):
        super(Teamwiseform, self).__init__(*args, **kwargs)
        self.fields['tw_project_code'].label_from_instance = lambda obj: "%s" % obj.project_code
        self.fields['tw_project_code'].widget.attrs['style'] = 'height:35px;'
        self.fields['manager'].label_from_instance = lambda obj: "%s" % obj.emp_name
        self.fields['manager'].widget.attrs['style'] = 'height:35px;'
        self.fields['department'].label_from_instance = lambda obj: "%s" % obj.department_name
        self.fields['department'].widget.attrs['style'] = 'height:35px;'
        self.fields['list_of_auditee'].label_from_instance = lambda obj: "%s" % obj.emp_name
        self.fields['list_of_auditee'].widget.attrs['style'] = 'height:35px;'
        self.helper = FormHelper()
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-lg-2'
        self.helper.layout = Layout(Field(
            'tw_project_code',
            'sub_code',
            'manager',
            'department',
            'team_manhours',
            'list_of_auditee'),
            ButtonHolder(
                Submit('submit', 'Submit', css_class='btn-success'),
                Reset('reset','Reset', css_class='btn-success'),
                HTML("""<a class= "btn btn-success" href= "{% url 'QMS:teamwiseview' %}"> Back</a>""")
            )
            )

    class Meta:
        model = Teamwise
        fields = ['tw_project_code','sub_code','manager','department','team_manhours','list_of_auditee']
