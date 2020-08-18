from django import forms
from QMS.models import EmployeeDetails, EmployePosition, EmployeDepartment
from django.urls import reverse
from QMS import default_choices
from crispy_forms.bootstrap import Field, InlineRadios, TabHolder, Tab,FormActions
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout, Div, Fieldset,Reset,Button,HTML,ButtonHolder
from django.db.models import Q


class EmployeeDetailsform(forms.ModelForm):

        emp_code = forms.CharField(max_length=3,label='Employee Code')
        emp_name = forms.CharField(max_length=50, label='Employee Name')
        emp_email = forms.EmailField(max_length=70, label='Employee Email')
        emp_department = forms.ModelChoiceField(queryset=EmployeDepartment.objects.all(),empty_label='--- Select ---')
        emp_position = forms.ModelChoiceField(queryset=EmployePosition.objects.all(),empty_label='--- Select ---')
        p1=EmployePosition.objects.get(emp_posn='Manager');p2=EmployePosition.objects.get(emp_posn='Team Lead');p3=EmployePosition.objects.get(emp_posn='General Manager')
        emp_reporting_to = forms.ModelChoiceField(queryset=EmployeeDetails.objects.filter(Q(emp_position=p1.id) | Q(emp_position=p2.id) | Q(emp_position=p3.id)),empty_label='--- Select ---')
        emp_approved_by = forms.ModelChoiceField(queryset=EmployeeDetails.objects.filter(Q(emp_position=p1.id) | Q(emp_position=p3.id)),empty_label='--- Select ---')
        emp_status = forms.ChoiceField(choices=default_choices.employ_status, label='Emplee Status')


        def __init__(self, *args, **kwargs):
            super(EmployeeDetailsform, self).__init__(*args, **kwargs)
            self.fields['emp_department'].label_from_instance = lambda obj: "%s" % obj.department_name
            self.fields['emp_department'].widget.attrs['style'] = 'height:35px;'
            self.fields['emp_position'].label_from_instance = lambda obj: "%s" % obj.emp_posn
            self.fields['emp_position'].widget.attrs['style'] = 'height:35px;'
            self.fields['emp_reporting_to'].label_from_instance = lambda obj: "%s" % obj.emp_name
            self.fields['emp_reporting_to'].widget.attrs['style'] = 'height:35px;'
            self.fields['emp_approved_by'].label_from_instance = lambda obj: "%s" % obj.emp_name
            self.fields['emp_approved_by'].widget.attrs['style'] = 'height:35px;'
            self.fields['emp_status'].widget.attrs['style'] = 'height:35px;'
            self.helper = FormHelper()
            #self.helper.form_method = 'post'
            #self.helper.form_action = reverse('audittype_view.html')
            self.helper.form_class = 'form-horizontal'
            self.helper.label_class = 'col-lg-4'
            self.helper.field_class = 'col-lg-8'
            # self.helper.add_input(Button('back',"Back",css_class='btn-success',onclick="{% url 'QMS:empdetailsview' %}"))
            self.helper.layout = Layout(Field(
                'emp_code',
                'emp_name',
                'emp_email',
                'emp_department',
                'emp_position',
                'emp_reporting_to',
                'emp_approved_by',
                'emp_status'),
                ButtonHolder(
                    Submit('submit', 'Submit', css_class='btn-success'),
                    Reset('reset','Reset', css_class='btn-success'),
                    HTML("""<a class= "btn btn-success" href= "{% url 'QMS:empdetailsview' %}"> Back</a>""")
                )
                )


        class Meta:
            """Meta Attributes"""
            model = EmployeeDetails
            fields = ['emp_code','emp_name','emp_email','emp_department','emp_position','emp_reporting_to','emp_approved_by','emp_status']
