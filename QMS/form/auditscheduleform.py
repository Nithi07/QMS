from django import forms
from QMS.models import Auditschedule
from QMS.models import ListAuditors
from QMS.models import Audittype
from QMS.models import EmployeeDetails
from QMS.models import EmployePosition
from QMS.models import Audit_comments
from QMS.models import ManualCheckList
from QMS.models import EmployeDepartment
from QMS.models import WorkManual
from QMS.models import Postpond,Cancel
from QMS.models import Project_Details,Teamwise
from django.urls import reverse
from crispy_forms.bootstrap import Field, InlineRadios, TabHolder, Tab,FormActions
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout, Div, Fieldset,Reset,Button,HTML,ButtonHolder
from django.db.models import Q
from dal import autocomplete

class Project_Detailsform(forms.ModelForm):
    project_code = forms.CharField(max_length=15,label = 'Project Code')
    project_name = forms.CharField(max_length=300,label = 'Project Name')
    project_type = forms.CharField(max_length=10,label = 'Type',initial='Project')
    project_start_date = forms.DateField(label = 'Start Date',required=True,widget=forms.TextInput(attrs={'type':'date'}))
    project_end_date = forms.DateField(label = 'End Date',required=True,widget=forms.TextInput(attrs={'type':'date'}))


    def __init__(self, *args, **kwargs):
        super(Project_Detailsform, self).__init__(*args, **kwargs)
        self.fields['project_type'].widget.attrs['readonly'] = True
        self.helper = FormHelper()
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-lg-2'
        self.helper.layout = Layout(Field(
            'project_code',
            'project_name',
            'project_type',
            'project_start_date',
            'project_end_date'),
            ButtonHolder(
                Submit('submit', 'Submit', css_class='btn-success'),
                Reset('reset','Reset', css_class='btn-success'),
                HTML("""<a class= "btn btn-success" href= "{% url 'QMS:projectview' %}"> Back</a>""")
            )
            )

    class Meta:
        model = Project_Details
        fields = ['project_code','project_name','project_type','project_start_date','project_end_date']


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


class Auditscheduleform(forms.ModelForm):
    schedule_auditype = forms.ModelChoiceField(queryset=Audittype.objects.all(),empty_label = 'Select', required=True, label = 'Audit Type')
    schedule_job_code = forms.CharField(max_length=15,label = 'Job Code')
    schedule_sub_job_code = forms.CharField(max_length=15,label = 'Sub JobCode')
    schedule_auditor_list = forms.ModelMultipleChoiceField(widget=forms.CheckboxSelectMultiple(),queryset=ListAuditors.objects.all(),label = 'Auditor List',required=True)
    schedule_auditee_list = forms.ModelMultipleChoiceField(widget=forms.CheckboxSelectMultiple(),queryset=Teamwise.objects.all(),label = 'Auditee List',required=True,)
    schedule_audit_date = forms.DateField(label = 'Audit Date',required=True,widget=forms.TextInput(attrs={'type':'date'}))
    schedule_audit_time = forms.TimeField(label = 'Audit Time',required=True,widget=forms.TextInput(attrs={'type':'time'}))
    schedule_iso_year = forms.ModelChoiceField(queryset=WorkManual.objects.all(),label = 'ISO Year',empty_label = 'Select',required=True)
    schedule_final_auditor_list  = forms.ModelMultipleChoiceField(widget=forms.CheckboxSelectMultiple(),queryset=ListAuditors.objects.all(),label = 'Final Auditor List',required=True)
    schedule_project = forms.ModelChoiceField(queryset=Project_Details.objects.all(),empty_label = 'Select',label = 'Project ID',widget=forms.HiddenInput())
    comment_status = forms.CharField(widget=forms.HiddenInput(),required=False,initial='Yet to Start')

    def __init__(self, *args, **kwargs):
        super(Auditscheduleform, self).__init__(*args, **kwargs)
        self.fields['schedule_auditype'].label_from_instance = lambda obj: "%s" % obj.audittype
        self.fields['schedule_auditype'].widget.attrs['style'] = 'height:40px;'
        self.fields['schedule_project'].label_from_instance = lambda obj: "%s" % obj.project_code
        self.fields['schedule_auditor_list'].label_from_instance = lambda obj: "%s" % obj.auditors.emp_name
        self.fields['schedule_auditee_list'].label_from_instance = lambda obj: "%s" % obj.list_of_auditee.emp_name
        self.fields['schedule_final_auditor_list'].label_from_instance = lambda obj: "%s" % obj.auditors.emp_name
        self.fields['schedule_iso_year'].label_from_instance = lambda obj: "%s" % obj.ISO_certification_year
        self.fields['schedule_iso_year'].widget.attrs['style'] = 'height:40px;'
        # self.fields['comment_status'].initial= 'Yet to Start'
        self.helper = FormHelper()
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-lg-2'
        self.helper.layout = Layout(Field(
            'schedule_auditype',
            'schedule_job_code',
            'schedule_sub_job_code',
            'schedule_audit_date',
            'schedule_audit_time',
            'schedule_auditee_list',
            'schedule_auditor_list',
            'schedule_iso_year',
            'schedule_final_auditor_list',
            'schedule_project',
            'comment_status')
            )

    class Meta:
        model = Auditschedule
        fields = ['schedule_auditype','schedule_job_code','schedule_project','schedule_sub_job_code','schedule_audit_date','schedule_audit_time',
                  'schedule_auditee_list','schedule_auditor_list','schedule_iso_year','schedule_final_auditor_list','comment_status']


class Confirmform(forms.Form):

    p1=EmployePosition.objects.get(emp_posn='Manager')
    schedule_department = forms.ModelChoiceField(
                        queryset=EmployeeDetails.objects.filter(Q(emp_position=p1.id)),
                        empty_label = '---Select---',required=False,widget=forms.Select(attrs={'class':'ddl'}))

    def __init__(self, *args, **kwargs):
        super(Confirmform, self).__init__(*args, **kwargs)
        self.fields['schedule_department'].label_from_instance = lambda obj: "%s" % obj.emp_name
        # self.fields['schedule_department'].widget.attrs['style'] = 'height:40px;'



class Postpondform(forms.ModelForm):
    post_date = forms.DateField(label = 'Postponed to',required=True,widget=forms.TextInput(
                                    attrs={'type':'date'}
                                    ))
    post_time = forms.TimeField(label = 'Postponed At',required=True,widget=forms.TextInput(
                                    attrs={'type':'time'}
                                    ))
    auditschedule_id = forms.CharField(max_length=5)

    def __init__(self, *args, **kwargs):
        super(Postpondform, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(Field(
            'post_date',
            'post_time',
            'auditschedule_id',
            'reason',
            ))


    class Meta:
        model = Postpond
        fields = ['post_date','post_time','reason','auditschedule_id']
        widgets = {
            'reason': forms.Textarea(attrs={'rows': 2, 'cols': 22}),
        }


class Cancelform(forms.ModelForm):
    cancelled_reason = forms.CharField(widget = forms.Textarea(attrs={'rows': 3, 'cols': 30}),required=True)

    def __init__(self, *args, **kwargs):
        super(Cancelform, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(Field(
            'cancelled_reason',
            ))

    class Meta:
        model = Cancel
        fields = ['cancelled_reason']


class ExportForm(forms.Form):
    audityear = forms.CharField(max_length=4)
    auditquarter = forms.CharField(max_length=10)
    auditype = forms.CharField(max_length=15,required=False)

class ExportProjectForm(forms.Form):
    audityear = forms.CharField(max_length=4)
    auditype = forms.CharField(max_length=15,required=False)
    project_code = forms.CharField(max_length=10,label = 'Project Code')
