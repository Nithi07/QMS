from django import forms
from QMS import default_choices
from QMS.models import Audittype
from QMS.models import WorkManual
from QMS.models import ManualCheckList
from django.forms import inlineformset_factory
from crispy_forms.bootstrap import Field, InlineRadios, TabHolder, Tab,FormActions
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout, Div, Fieldset,Reset,Button,HTML,ButtonHolder
from QMS.custom_layout_object import Formset


class WorkManualform(forms.ModelForm):

    audit_typ = forms.ModelMultipleChoiceField(widget=forms.CheckboxSelectMultiple(),queryset=Audittype.objects.all(),label='Audit Type')
    cls_ref_no = forms.CharField(max_length=10,label="Cls Ref No")
    activity_title = forms.CharField(max_length=100,label='Activity Title')
    ISO_certification_year = forms.CharField(max_length=50,label='ISO Year')
    type_of_projectortender = forms.MultipleChoiceField(choices=default_choices.type,widget=forms.CheckboxSelectMultiple(),label='Project/Tender',required=True)

    def __init__(self, *args, **kwargs):
        super(WorkManualform, self).__init__(*args, **kwargs)
        self.fields['audit_typ'].label_from_instance = lambda obj: "%s" % obj.audittype
        self.helper = FormHelper()
        self.helper.add_input(Submit('submit', 'Submit', css_class='btn-success'))
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-lg-2'
        self.helper.layout = Layout(
            Div(
                Field('audit_typ'),
                Field('cls_ref_no'),
                Field('activity_title'),
                Field('ISO_certification_year'),
                Field('type_of_projectortender'),
                Field('checklist'),

                Formset('activity'),
                ButtonHolder(
                    Submit('submit', 'Submit', css_class='btn-success'),
                    Reset('reset','Reset', css_class='btn-success'),
                    HTML("""<a class= "btn btn-success" href= "{% url 'QMS:workmanualview' %}"> Back</a>""")
                 )
                )
            )

    class Meta:
        model = WorkManual
        fields = ['audit_typ','cls_ref_no','activity_title','ISO_certification_year','type_of_projectortender',
                  ]


class ManualCheckListForm(forms.ModelForm):
    checklist = forms.CharField(
            widget = forms.Textarea(attrs={'rows': 2, 'cols': 22}),
            required = True,label='Checklist'
            )

    class Meta:
        model = ManualCheckList
        fields = ['checklist']


ManualCheckListFormSet = inlineformset_factory(WorkManual, ManualCheckList, form=ManualCheckListForm,extra=1, can_delete=True)
