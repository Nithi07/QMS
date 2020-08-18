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
from Timesheet.settings import DATE_INPUT_FORMATS,TIME_INPUT_FORMATS
from crispy_forms.bootstrap import Field, InlineRadios, TabHolder, Tab,FormActions
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout, Div, Fieldset,Reset,Button,HTML,ButtonHolder
from django.db.models import Q
# from django.forms import extras
# from generic.forms.widgets import SelectTimeWidget

class Auditscheduleform(forms.ModelForm):

    schedule_auditype = forms.ModelChoiceField(queryset=Audittype.objects.all(),empty_label = 'Select', required=True, label = 'Audit Type')
    schedule_job_code = forms.CharField(max_length=15,label = 'Job Code')
    schedule_sub_job_code = forms.CharField(max_length=15,label = 'Sub JobCode',required=False)
    schedule_auditor_list = forms.ModelMultipleChoiceField(widget=forms.CheckboxSelectMultiple(),queryset=ListAuditors.objects.all(),label = 'Auditor List',required=True)
    schedule_auditee_list = forms.ModelMultipleChoiceField(widget=forms.CheckboxSelectMultiple(),queryset=EmployeeDetails.objects.none(),label = 'Auditee List',required=True,)
    schedule_audit_date = forms.DateField(label = 'Audit Date',required=True,input_formats=DATE_INPUT_FORMATS,widget=forms.DateInput(attrs={'id':'datepicker'},format='%d-%m-%Y'))
    schedule_audit_time = forms.TimeField(label = 'Audit Time',required=True,input_formats=TIME_INPUT_FORMATS,widget=forms.TimeInput(attrs={'class':'timepicker'},format='%H:%M'))
    schedule_iso_year = forms.ModelChoiceField(queryset=WorkManual.objects.all().distinct('ISO_certification_year'),label = 'ISO Year',empty_label = 'Select',required=True)
    p1=EmployePosition.objects.get(emp_posn='Manager');p2=EmployePosition.objects.get(emp_posn='Team Lead');p3=EmployePosition.objects.get(emp_posn='General Manager');p4=EmployePosition.objects.get(emp_posn='Cheif Manager')
    p5=EmployePosition.objects.get(emp_posn='Director');p6=EmployePosition.objects.get(emp_posn='DGM')
    schedule_final_auditor_list  = forms.ModelMultipleChoiceField(widget=forms.CheckboxSelectMultiple(),queryset=EmployeeDetails.objects.filter(Q(emp_position=p1.id)|Q(emp_position=p2.id)|Q(emp_position=p3.id)|Q(emp_position=p4.id)|Q(emp_position=p5.id)|Q(emp_position=p6.id)),label = 'Final Auditor List',required=True)
    schedule_project = forms.ModelChoiceField(queryset=Project_Details.objects.all(),empty_label = 'Select',label = 'Project ID')
    create_by = forms.CharField(widget=forms.HiddenInput(),max_length=15,required=False)
    create_on = forms.DateTimeField(widget=forms.HiddenInput(),required=False)
    create_ip = forms.GenericIPAddressField(widget=forms.HiddenInput(),required=False)



    def __init__(self, *args, **kwargs):
        queryset=kwargs.pop('queryset', None)
        super(Auditscheduleform, self).__init__(*args, **kwargs)
        self.fields['schedule_auditype'].label_from_instance = lambda obj: "%s" % obj.audittype
        self.fields['schedule_auditype'].widget.attrs['style'] = 'height:40px;'
        self.fields['schedule_project'].label_from_instance = lambda obj: "%s" % obj.project_code
        self.fields['schedule_auditor_list'].label_from_instance = lambda obj: "%s" % obj.auditors.emp_name
        self.fields['schedule_auditee_list'].label_from_instance = lambda obj: "%s" % obj.emp_name
        self.fields['schedule_final_auditor_list'].label_from_instance = lambda obj: "%s" % obj.emp_name
        self.fields['schedule_iso_year'].label_from_instance = lambda obj: "%s" % obj.ISO_certification_year
        self.fields['schedule_iso_year'].widget.attrs['style'] = 'height:40px;'

        if 'schedule_job_code' in self.data:
            try:
                pro_id = Project_Details.objects.get(project_code=self.data.get('schedule_job_code'))
                team_id = Teamwise.objects.filter(tw_project_code_id=pro_id)
                emp_det_id = (i.list_of_auditee_id for i in team_id)
                self.fields['schedule_auditee_list'].queryset = EmployeeDetails.objects.filter(id__in=emp_det_id)
            except (ValueError,TypeError):
                pass
        elif self.instance.pk:
            self.fields['schedule_auditee_list'].queryset = self.instance.schedule_auditee_list

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
            'create_by',
            'create_on',
            'create_ip',
            )
            )

    class Meta:
        model = Auditschedule
        fields = ['schedule_auditype','schedule_job_code','schedule_project','schedule_sub_job_code','schedule_audit_date','schedule_audit_time',
                  'schedule_auditee_list','schedule_auditor_list','schedule_iso_year','schedule_final_auditor_list','create_by','create_on','create_ip',]


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
    post_date = forms.DateField(label = 'Postponed to',required=True,input_formats=DATE_INPUT_FORMATS,widget=forms.DateInput(attrs={'class':'datepicker'},format='%d-%m-%Y'))
    post_time = forms.TimeField(label = 'Postponed At',required=True,input_formats=TIME_INPUT_FORMATS,widget=forms.TimeInput(attrs={'class':'timepicker'},format='%H:%M'))
    auditschedule_id = forms.IntegerField(widget=forms.HiddenInput(),required=False)

    def __init__(self, *args, **kwargs):
        super(Postpondform, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(Field(
            'auditschedule_id',
            'post_date',
            'post_time',
            'reason',
            ))


    class Meta:
        model = Postpond
        fields = ['auditschedule_id','post_date','post_time','reason']
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
    audityear = forms.CharField(max_length=4,required=False)
    auditype = forms.CharField(max_length=15,required=False)
    project_code = forms.CharField(max_length=10,label = 'Project Code')
