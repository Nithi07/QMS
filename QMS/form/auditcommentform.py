from django import forms
from multivaluefield import MultiValueField
from QMS import default_choices
from QMS.models import Auditschedule
from QMS.models import ListAuditors
from QMS.models import Audittype
from QMS.models import EmployeeDetails
from QMS.models import Audit_comments
from QMS.models import NCR_Comment
from QMS.models import ManualCheckList
from QMS.models import EmployeDepartment
from django.urls import reverse
from crispy_forms.bootstrap import Field, InlineRadios, TabHolder, Tab,FormActions
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout, Div, Fieldset,Reset,Button,HTML,ButtonHolder
from django.forms import inlineformset_factory,modelformset_factory
from QMS.custom_layout_object import Formset


class Auditor_commentsForm(forms.ModelForm):

    cls_refno = forms.CharField(widget = forms.TextInput(attrs={'readonly':'readonly'}))
    description = forms.CharField(widget = forms.Textarea(attrs={'rows': 3, 'cols': 30,'readonly':'readonly'}))
    auditor_comments = forms.CharField(widget = forms.Textarea(attrs={'rows': 3, 'cols': 50}))
    comment_status = forms.ChoiceField(choices=default_choices.status)
    department = forms.ModelChoiceField(queryset=EmployeDepartment.objects.all(),required=False,empty_label = '--- Select ---')

    def __init__(self, *args, **kwargs):
        super(Auditor_commentsForm, self).__init__(*args, **kwargs)
        self.fields['department'].label_from_instance = lambda obj: "%s" % obj.dept_code
        self.fields['comment_status'].widget.attrs['style'] = 'height:30px;'
        self.fields['department'].widget.attrs['style'] = 'height:30px;'
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Div(
                Field('cls_refno'),
                Field('description'),
                Field('auditor_comments'),
                Field('comment_status'),
                Field('department'),
                )
            )

    class Meta:
        model = Audit_comments
        fields = ['cls_refno','description','auditor_comments','comment_status','department']

Auditor_commentsFormset = modelformset_factory(Audit_comments,form=Auditor_commentsForm,extra=0)


class Auditee_commentsForm(forms.ModelForm):

    auditee_status = forms.ChoiceField(choices=default_choices.auditeechoice)
    auditee_correction = forms.CharField(widget=forms.Textarea(attrs={'rows': 3, 'cols': 70}))

    def __init__(self, *args, **kwargs):
        super(Auditee_commentsForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Div(
                Field('auditee_status'),
                Field('auditee_correction'),
                )
            )
    class Meta:
        model = Audit_comments
        fields = ['auditee_correction','auditee_status']


class NCR_commentsForm(forms.ModelForm):

    root_cause_analysis = forms.CharField(
            widget = forms.Textarea(attrs={'rows': 3, 'cols': 70}),
            required = True
            )
    correction = forms.CharField(
            widget = forms.Textarea(attrs={'rows': 3, 'cols': 70}),
            required = True
            )
    corrective_action = forms.CharField(
            widget = forms.Textarea(attrs={'rows': 3, 'cols': 70}),
            required = True
            )

    def __init__(self, *args, **kwargs):
        super(NCR_commentsForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Div(
                Field('root_cause_analysis'),
                Field('correction'),
                Field('corrective_action'),
                )
            )

    class Meta:
        model = NCR_Comment
        fields = ['root_cause_analysis','correction','corrective_action']



class Verified_commentsForm(forms.ModelForm):

    verified_status = forms.ChoiceField(choices=default_choices.verifychoice)

    def __init__(self, *args, **kwargs):
        super(Verified_commentsForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Div(
                Field('verified_comments'),
                Field('verified_status'),
                )
            )
    class Meta:
        model = Audit_comments
        fields = ['verified_comments','verified_status',]
        widgets = {
            'verified_comments': forms.Textarea(attrs={'rows': 3, 'cols': 50}),
        }

class mr_commentsForm(forms.ModelForm):

    mr_status = forms.ChoiceField(choices=default_choices.mr_choice)
    mr_comments = forms.CharField(widget=forms.Textarea(attrs={'rows': 2, 'cols': 22}))

    def __init__(self, *args, **kwargs):
        super(mr_commentsForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Div(
                Field('mr_comments'),
                Field('mr_status'),
                )
            )
    class Meta:
        model = Audit_comments
        fields = ['mr_comments','mr_status',]
