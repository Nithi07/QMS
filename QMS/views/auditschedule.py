from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from QMS.models import Auditschedule
from QMS.models import Project_Details,Teamwise
from QMS.models import Teamwise
from QMS.models import EmployeeDetails
from QMS.models import Audittype
from QMS.models import WorkManual
from QMS.models import ManualCheckList
from QMS.models import Audit_comments
from QMS.models import Postpond,Cancel
from QMS.models import NCR_Comment
from QMS.views.mailgenerate import Mail
from QMS.form.project_teamwiseform import Project_Detailsform,Teamwiseform
from QMS.form.auditscheduleform import Auditscheduleform
from QMS.form.auditscheduleform import Postpondform
from QMS.form.auditscheduleform import Cancelform
from QMS.form.auditscheduleform import Confirmform
from QMS.form.auditscheduleform import ExportForm, ExportProjectForm
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView,View,FormView
from django.urls import  reverse_lazy
from django.contrib import messages
from datetime import datetime, date
from django.db.models import Q
import xlsxwriter
from xlsxwriter.workbook import Workbook
from Timesheet.settings import EMAIL_HOST_USER
from django.core.mail import send_mail,EmailMultiAlternatives,EmailMessage
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.db.models import F
# from django.db.models.expressions import CombinedExpression, Value
import json
from django.http import JsonResponse



class MRconfirm(ListView):
    model = Auditschedule
    template_name = 'superadmin/email_mr_auditschedule.html'

    def get_context_data(self, **kwargs):
        auditschedule = Auditschedule.objects.filter(schedule_department_status=1).filter(schedule_audit_mr_status=0).order_by('pk')
        obj = {'auditschedule':auditschedule,'mail':0}
        return obj

    def Sendmail(request):
        subject = 'Audit schedule for this Quarter'
        auditschedule=Auditschedule.objects.filter(schedule_department_status=1).filter(schedule_audit_mr_status=0).order_by('pk')
        html_content = render_to_string('superadmin/email_mr_auditschedule.html',{'auditschedule':auditschedule,'mail':1})
        plain_message = strip_tags(html_content)
        to, cc = [],[]
        for i in Auditschedule.objects.filter(schedule_department_status=1).filter(schedule_audit_mr_status=0):
            [to.append(j.emp_email) for j in i.schedule_auditee_list.all() if j.emp_email not in to]
            [to.append(j.auditors.emp_email) for j in i.schedule_auditor_list.all() if j.auditors.emp_email not in to]
            [cc.append(j.emp_email) for j in i.schedule_final_auditor_list.all() if j.emp_email not in cc]
            i.schedule_audit_mr_status = 1
            i.audit_comment_status = 1
            i.save()

        if len(to) == 0:
            messages.success(request, 'Mail Send Failed \U0001F44E \U0001F44E \U0001F44E')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        else:
            return Mail.mailgenerate(request,subject,plain_message,EMAIL_HOST_USER,to,cc,html_content)



# Auditschedule ListView
class AuditscheduleListview(ListView):
    model = Auditschedule
    template_name = 'superadmin/auditshedule_view.html'
    def get_context_data(self, **kwargs):
        auditcomments = Audit_comments.objects.all()
        auditschedule = Auditschedule.objects.filter(Q(schedule_status=0)|Q(schedule_status=1)).order_by('pk')
        postpond_schedules = Postpond.objects.all()
        obj = {'auditschedule':auditschedule,'postpond_schedules':postpond_schedules,'postpond_id':[i.auditschedule_id for i in Postpond.objects.all()]}
        return obj


class AuditscheduleConfirmListview(CreateView):
    model = Auditschedule
    form_class = Confirmform
    template_name = 'superadmin/auditschedule_confirm.html'
    success_url = 'QMS:auditscheduleview'

    def get_success_url(self):
        return reverse_lazy(self.success_url)

    def get_context_data(self):
        auditschedule = Auditschedule.objects.get(pk=self.kwargs['pk'])
        self.request.session['instance'] = auditschedule.id
        confirmed_managers =  auditschedule.schedule_department_username
        confirming_managers = [o.emp_approved_by.emp_name for o in auditschedule.schedule_auditee_list.all()]
        jobs = Auditschedule.objects.filter(schedule_job_code=auditschedule.schedule_job_code)
        project_code_data = {}
        for i in jobs:
            if i.schedule_auditype.audittype not in project_code_data:
                project_code_data[i.schedule_auditype.audittype] = {'auditconducted':0,'Completed':0,'InProgress':0}
            project_code_data[i.schedule_auditype.audittype]['auditconducted'] += 1
            if i.schedule_status == 1:
                project_code_data[i.schedule_auditype.audittype]['Completed'] += 1
            elif i.schedule_status == 0:
                project_code_data[i.schedule_auditype.audittype]['InProgress'] += 1
        obj = {'auditschedule':auditschedule,"form":Confirmform(),'project_code_data':project_code_data,
                'confirming_managers':confirming_managers,'confirmed_managers':confirmed_managers}
        return obj


    def save(request, manager_name):
        schedule_id = request.session.get('instance')
        instance = Auditschedule.objects.get(pk=schedule_id)
        print(instance.schedule_department_username)
        if instance.schedule_department_username == None:
            Auditschedule.objects.filter(pk=schedule_id).update(schedule_department_username=manager_name,schedule_department_date=datetime.today().date())
        elif manager_name in instance.schedule_department_username:
            pass
        else:
            instance.schedule_department_username.append(manager_name)
            instance.schedule_department_date.append(datetime.today().date())
            instance.save()

        if instance.schedule_department_username == None:
            pass
        elif len(instance.schedule_department_username) == len([o.emp_approved_by.emp_name for o in instance.schedule_auditee_list.all()]):
            Q1, Q2, Q3, Q4 = ['01','02','03'], ['04','05','06'], ['07','08','09'], ['10','11','12']
            ac = []
            auditype = instance.schedule_auditype.auditcode
            ad = instance.schedule_audit_date
            auditdate = str(ad).split('-')
            ac.append(auditype)
            apnd = ac.append('Q1') if auditdate[1] in Q1 else ac.append('Q2') if auditdate[1] in Q2 else ac.append('Q3') if auditdate[1] in Q3 else ac.append('Q4')
            ac.append(auditdate[0])
            ac.append(str(instance.id))
            auditcode = '/'.join(ac)
            instance.schedule_audit_code = auditcode
            instance.schedule_department_status = 1
            instance.save()
        return redirect('QMS:auditscheduleview')

    #
    # def form_valid(self,form,request):
    #     instance = Auditschedule.objects.get(pk=self.kwargs['pk'])
    #     a_name = request.POST.getlist('schedule_department')
    #     if instance.schedule_department_username == None:
    #         Auditschedule.objects.filter(pk=self.kwargs['pk']).update(schedule_department_username=[EmployeeDetails.objects.get(id=a_name[0]).emp_name],schedule_department_date=datetime.today())
    #     elif EmployeeDetails.objects.get(id=a_name[0]).emp_name in instance.schedule_department_username:
    #         pass
    #     else:
    #         instance.schedule_department_username.append(EmployeeDetails.objects.get(id=a_name[0]).emp_name)
    #         instance.schedule_department_date.append(datetime.today())
    #         instance.save()
    #
    #     if instance.schedule_department_username == None:
    #         pass
    #     elif len(instance.schedule_department_username) == len(set([o.emp_approved_by.emp_name for o in instance.schedule_auditee_list.all()])):
    #         Q1, Q2, Q3, Q4 = ['01','02','03'], ['04','05','06'], ['07','08','09'], ['10','11','12']
    #         ac = []
    #         auditype = instance.schedule_auditype.auditcode
    #         ad = instance.schedule_audit_date
    #         auditdate = str(ad).split('-')
    #         ac.append(auditype)
    #         apnd = ac.append('Q1') if auditdate[1] in Q1 else ac.append('Q2') if auditdate[1] in Q2 else ac.append('Q3') if auditdate[1] in Q3 else ac.append('Q4')
    #         ac.append(auditdate[0])
    #         ac.append(str(instance.id))
    #         auditcode = '/'.join(ac)
    #         instance.schedule_audit_code = auditcode
    #         instance.schedule_department_status = 1
    #         instance.save()
    #     return HttpResponseRedirect(self.get_success_url())
    #

def ajax_response(request):
    q = request.GET.get('schedule_job_code')
    qs = Project_Details.objects.get(project_code=q)
    projects = Teamwise.objects.filter(tw_project_code=qs)
    return render(request, 'superadmin/auditee_list_options.html', {'projects':projects})

def ajax_hidden(request):
    q = request.GET.get('schedule_job_code')
    qs = Project_Details.objects.get(project_code=q)
    return render(request, 'superadmin/project_type_options.html', {'option':qs})


# Auditschedule CreateView
class AuditscheduleCreate(CreateView):
    model = Auditschedule
    form_class = Auditscheduleform
    success_url = 'QMS:auditscheduleview'
    template_name = 'superadmin/auditshedule_form.html'


    def get_success_url(self):
       return reverse_lazy(self.success_url)

    def post(self, request, *args, **kwargs):
        form = Auditscheduleform(request.POST)
        # import pdb; pdb.set_trace()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)
            messages.error(request, 'The form is invalid')

    def form_valid(self, form):
        obj = form.save(commit=False)
        schedule_iso_year = form.cleaned_data['schedule_iso_year']
        obj.schedule_iso_year = schedule_iso_year.ISO_certification_year
        obj.create_by = 'admin'
        obj.create_on = datetime.today()
        obj.create_ip = '192.168.2.14'
        obj.save()
        form.save_m2m()
        return HttpResponseRedirect(self.get_success_url())


class AuditscheduleUpdate(UpdateView):
     model = Auditschedule
     form_class = Auditscheduleform
     success_url = 'QMS:auditscheduleview'
     template_name = 'superadmin/auditshedule_form.html'

     def get_success_url(self):
        return reverse_lazy(self.success_url)

     def form_valid(self, form):
        form = self.get_form()
        form.save()
        return HttpResponseRedirect(self.get_success_url())


#Auditschedule DeleteView
class AuditscheduleDelete(DeleteView):
    def ObjectDelete(request,pk):
        object=Auditschedule.objects.get(id=pk)
        object.delete()
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


class AuditschedulePostpond(CreateView):
    model = Postpond
    form_class = Postpondform
    success_url = 'QMS:auditscheduleview'
    template_name = 'superadmin/postpond_form.html'

    def get_context_data(self, **kwargs):
        context = super(AuditschedulePostpond, self).get_context_data(**kwargs)
        context["auditschedule"] = Auditschedule.objects.get(pk=self.kwargs.get("pk"))
        return context

    def post(self, request, *args, **kwargs):
        form = Postpondform(request.POST)
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self,form):
        obj = form.save(commit=False)
        obj.auditschedule = Auditschedule.objects.get(id=self.kwargs.get("pk"))
        # Postpond.objects.create(post_date=request.POST.get('post_date'),post_time=request.POST.get('post_time'),reason=request.POST.get('reason'),
        obj.save()
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
       return reverse_lazy(self.success_url)

class AuditschedulePostpondUpdate(UpdateView):
    model = Postpond
    form_class = Postpondform
    success_url = 'QMS:auditscheduleview'
    template_name = 'superadmin/postpond_form.html'

    def get_context_data(self, **kwargs):
        context = super(AuditschedulePostpondUpdate, self).get_context_data(**kwargs)
        context["auditschedule"] = Auditschedule.objects.get(pk=self.kwargs.get("pk"))
        return context

    def form_valid(self,form):
        form = self.get_form()
        form.save()
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
       return reverse_lazy(self.success_url)


class AuditscheduleCancel(CreateView):
    model = Cancel
    form_class = Cancelform
    template_name = 'superadmin/auditschedule_cancel.html'
    success_url = 'QMS:auditscheduleview'

    def get_context_data(self, **kwargs):
        context = super(AuditscheduleCancel, self).get_context_data(**kwargs)
        context["auditschedule"] = Auditschedule.objects.get(pk=self.kwargs.get("pk"))
        return context

    def post(self, request, *args, **kwargs):
        form = Cancelform(request.POST)
        if form.is_valid():
            return self.form_valid(form,request)
        else:
            return self.form_invalid(form)

    def form_valid(self,form,request):
        Cancel.objects.create(cancelled_reason = request.POST.get('cancelled_reason'),modified_by='admin',modified_ip='192.168.2.14',
         auditschedule=Auditschedule.objects.get(id=self.kwargs.get("pk")))

        Auditschedule.objects.filter(pk=self.kwargs.get("pk")).update(schedule_status = 2)
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
       return reverse_lazy(self.success_url)


def AuditscheduleClosed(request, id):#not mention id instead of pk in url
    Auditschedule.objects.filter(id=id).update(schedule_status = 1,audit_comment_status = 7)
    for ncc in NCR_Comment.objects.filter(audit_id=id):
        ncc.ncr_closed_on = datetime.today()
        ncc.save()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


class AuditscheduleExportTable(FormView):
    form_class = ExportForm
    template_name = 'superadmin/auditschedule_report_form.html'

    def post(self, request, *args, **kwargs):
        form = ExportForm(request.POST)
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self,form):
        aud_yr = self.request.POST.get('audityear')
        aud_qua = self.request.POST.get('auditquarter')
        a_type = self.request.POST.get('auditype')
        # export form data to another function using session
        self.request.session['audityear'] = self.request.POST['audityear']
        self.request.session['auditquarter'] = self.request.POST['auditquarter']
        self.request.session['auditype'] = self.request.POST['auditype']
        rows = []
        audit_status = []
        for fil in Auditschedule.objects.all():
            audit_status.append('Yet to start') if fil.audit_comment_status == 0 else audit_status.append('Auditor and Auditee to Respond') if fil.audit_comment_status == 1 else audit_status.append('Auditor to Respond') if fil.audit_comment_status == 2 else audit_status.append('Auditee to Respond') if fil.audit_comment_status == 3 else audit_status.append('Auditor to Verify') if fil.audit_comment_status == 4 else audit_status.append('MR to Respond') if fil.audit_comment_status == 5 else audit_status.append('Waiting for Closed') if fil.audit_comment_status == 6 else audit_status.append('Completed')
            if fil.schedule_audit_code != None:
                spl = fil.schedule_audit_code.split('/')
                if (spl[1] == aud_qua and spl[2] == aud_yr and a_type=='') or (spl[1]==aud_qua and spl[2]==aud_yr and a_type==fil.schedule_auditype.audittype):
                    ncr_cou = 0
                    ncr_closed = 0
                    for ac in Audit_comments.objects.filter(auditschedule=fil.id,comment_status=2):
                        ncr_cou += 1
                        try:
                            cou = NCR_Comment.objects.get(command_id=ac.id)
                        except:
                            continue
                        if cou.ncr_closed_on != None:
                            ncr_closed += 1
                    rows.append([fil.schedule_audit_code,fil.schedule_auditee_list.all(),fil.schedule_job_code,
                                '','',fil.schedule_auditor_list.all(),fil.schedule_audit_date.strftime('%d-%m-%Y'),
                                str(fil.modified_on.date().strftime('%d-%m-%Y')),ncr_cou,ncr_closed,'',audit_status[0]])
            audit_status.clear()
        F, S, T = ['01','04','07','10'], ['02','05','08','11'], ['03','06','09','12']
        lis1 = []
        for row in rows:
            spl = row[6].split('-')
            lis2 = []
            for col_num in range(len(row)):
                if col_num == 1:
                    lis2.append( '/ '.join([x.emp_name for x in row[col_num]]))
                elif col_num == 2:
                    if spl[1] in F:
                        lis2.append(row[2])
                    else:
                        lis2.append('')
                elif col_num == 3:
                    if spl[1] in S:
                        lis2.append(row[2])
                    else:
                        lis2.append('')
                elif col_num == 4:
                    if spl[1] in T:
                        lis2.append(row[2])
                    else:
                        lis2.append('')
                elif col_num == 5:
                    lis2.append('/ '.join([x.auditors.emp_name for x in row[col_num]]))
                else:
                    lis2.append(row[col_num])
            spl.clear()
            lis1.append(lis2[0::])
            lis2.clear()
        month = []
        if str(aud_qua) == 'Q1':
            month.append("Jan")
            month.append("Feb")
            month.append("Mar")
        elif str(aud_qua) == 'Q2':
            month.append("Apr")
            month.append("May")
            month.append("Jun")
        elif str(aud_qua) == 'Q3':
            month.append("Jul")
            month.append("Aug")
            month.append("Sep")
        elif str(aud_qua) == 'Q4':
            month.append("Oct")
            month.append("Nov")
            month.append("Dec")
        dic = {'details':lis1,'month':month,'quater':aud_qua[1]}
        return render(self.request,'superadmin/schedule_report.html',dic )


    def export(request):
        # import form datas from above function using session
        aud_yr = request.session.get('audityear')
        aud_qua = request.session.get('auditquarter')
        a_type = request.session.get('auditype')

        response = HttpResponse(content_type='ms-excel')
        response['Content-Disposition'] = 'attachment; filename="auditschedule_report.xlsx"'

        wb = Workbook(response,{'default_date_format':'dd/mm/yy'})
        ws = wb.add_worksheet('Auditschedule')
        date_time = 'Date',str(datetime.today().strftime('%d-%m-%Y'))
        date = ':'.join(date_time)
        merge_format1 = wb.add_format({
                        'border':1,
                        'align':'center',
                        'valign':'vcenter',
                        'text_wrap':True,
                        'bold':True,
                        })
        merge_format2 = wb.add_format({
                        'border':1,
                        'align':'center',
                        'valign':'vcenter',
                        'text_wrap':True,
                        })
        border_format = wb.add_format({'border':1})
        ws.merge_range("A1:L1",'4A DESIGN & ENGINEERING PVT LTD.',merge_format1)
        ws.set_column(2,0,20,border_format)
        ws.set_column(3,0,20,border_format)
        ws.set_column(2,1,30,border_format)
        ws.set_column(3,1,30,border_format)
        ws.set_column('C:C',9,border_format)
        ws.set_column('D:D',9,border_format)
        ws.set_column('E:E',9,border_format)
        ws.set_column('F:F',30,border_format)
        ws.set_column('G:G',14,border_format)
        ws.set_column('H:H',15,border_format)
        ws.set_column('I:I',8.4,border_format)
        ws.set_column('J:J',8.4,border_format)
        ws.set_column('K:K',10,border_format)
        ws.set_column('L:L',13,border_format)

        ws.merge_range("A2:C2",'Document No:4A:FRM:09',merge_format1)
        ws.write(1,3,"Issue:1",merge_format1)
        ws.merge_range("E2:I2",'INTERNAL QUALITY AUDIT SCHEDULE FOR THE QUARTER'+' '+aud_qua[1],merge_format1)
        ws.write(1,9,"Rev No:C",merge_format1)

        ws.merge_range("K2:L2",'Date:31.07.2015',merge_format1)
        ws.merge_range("A3:A4",'Audit No',merge_format1)
        ws.merge_range("B3:B4",'Auditee Team',merge_format1)
        ws.merge_range("C3:E3",'Jobs to be Audited During the Period',merge_format1)
        ws.merge_range("F3:F4",'Auditor Nominated',merge_format1)
        ws.merge_range("G3:G4",'Scheduled Audit Date',merge_format1)
        ws.merge_range("H3:H4",'Audit Carried out on',merge_format1)
        ws.merge_range("I3:J3",'No of NCR',merge_format1)
        ws.merge_range("K3:K4",'Remarks',merge_format1)
        ws.merge_range("L3:L4",'Status of Audit',merge_format1)

        if str(aud_qua) == 'Q1':
            ws.write(3,2,"Jan",merge_format1)
            ws.write(3,3,"Feb",merge_format1)
            ws.write(3,4,"Mar",merge_format1)
        elif str(aud_qua) == 'Q2':
            ws.write(3,2,"Apr",merge_format1)
            ws.write(3,3,"May",merge_format1)
            ws.write(3,4,"Jun",merge_format1)
        elif str(aud_qua) == 'Q3':
            ws.write(3,2,"Jul",merge_format1)
            ws.write(3,3,"Aug",merge_format1)
            ws.write(3,4,"Sep",merge_format1)
        elif str(aud_qua) == 'Q4':
            ws.write(3,2,"Oct",merge_format1)
            ws.write(3,3,"Nov",merge_format1)
            ws.write(3,4,"Dec",merge_format1)
        ws.write("I4","Issued",merge_format1)
        ws.write("J4","Closed",merge_format1)
        rows = []
        audit_status = []
        for fil in Auditschedule.objects.all():
            audit_status.append('Yet to start') if fil.audit_comment_status == 0 else audit_status.append('Auditor and Auditee to Respond') if fil.audit_comment_status == 2 else audit_status.append('Verified') if fil.audit_comment_status == 3 else audit_status.append('MR status') if fil.audit_comment_status == 4 else audit_status.append('Completed')
            if fil.schedule_audit_code != None:
                spl = fil.schedule_audit_code.split('/')
                if (spl[1] == aud_qua and spl[2] == aud_yr and a_type=='') or (spl[1]==aud_qua and spl[2]==aud_yr and a_type==fil.schedule_auditype.audittype):
                    ncr_cou = 0
                    ncr_closed = 0
                    for ac in Audit_comments.objects.filter(auditschedule=fil.id,comment_status=2):
                        ncr_cou += 1
                        try:
                            cou = NCR_Comment.objects.get(command_id=ac.id)
                        except:
                            continue
                        if cou.ncr_closed_on != None:
                            ncr_closed += 1
                    rows.append([fil.schedule_audit_code,fil.schedule_auditee_list.all(),fil.schedule_job_code,
                                '','',fil.schedule_auditor_list.all(),fil.schedule_audit_date.strftime('%d-%m-%Y'),
                                str(fil.modified_on.date().strftime('%d-%m-%Y')),ncr_cou,ncr_closed,'',audit_status[0]])
            audit_status.clear()

        F, S, T = ['01','04','07','10'], ['02','05','08','11'], ['03','06','09','12']

        row_num = 3
        for row in rows:
            row_num += 1
            spl = row[6].split('-')
            for col_num in range(len(row)):
                if col_num == 1:
                    ws.write(row_num, col_num, '/ '.join([x.emp_name for x in row[col_num]]),merge_format2)
                elif col_num == 5:
                    ws.write(row_num, col_num, '/ '.join([x.auditors.emp_name for x in row[col_num]]),merge_format2)
                elif col_num == 2:
                    if spl[1] in F:
                        ws.write(row_num, col_num, row[2],merge_format2)
                    else:
                        ws.write(row_num, col_num, '',merge_format2)
                elif col_num == 3:
                    if spl[1] in S:
                        ws.write(row_num, col_num, row[2],merge_format2)
                    else:
                        ws.write(row_num, col_num, '',merge_format2)
                elif col_num == 4:
                    if spl[1] in T:
                        ws.write(row_num, col_num, row[2],merge_format2)
                    else:
                        ws.write(row_num, col_num, '',merge_format2)
                else:
                    ws.write(row_num, col_num, row[col_num],merge_format2)
        wb.close()
        return response


class NCRExportTable(FormView):
    form_class = ExportForm
    template_name = 'superadmin/ncr_report_form.html'

    def post(self, request, *args, **kwargs):
        form = ExportForm(request.POST)
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self,form):
        aud_yr = self.request.POST.get('audityear')
        aud_qua = self.request.POST.get('auditquarter')
        a_type = self.request.POST.get('auditype')
        # export form data to another function using session
        self.request.session['audityear'] = self.request.POST['audityear']
        self.request.session['auditquarter'] = self.request.POST['auditquarter']
        self.request.session['auditype'] = self.request.POST['auditype']
        rows = []
        nc_cmt_id = [i.id for i in Audit_comments.objects.all()]
        for nc in NCR_Comment.objects.all():
            if nc.command_id in nc_cmt_id:
                aud_sch = Auditschedule.objects.get(pk=nc.audit_id)
                ac = Audit_comments.objects.get(pk=nc.command_id)
                ncr_closed_date = '' if nc.ncr_closed_on == None else str(nc.ncr_closed_on.date().strftime('%d-%m-%Y'))
                if ac.comment_status == 2:
                    spl = nc.ncr_code.split('-')
                    if (spl[2] == aud_qua and spl[1] == aud_yr and a_type==aud_sch.schedule_auditype.audittype) or (spl[2] == aud_qua and spl[1] == aud_yr and a_type==""):
                        rows.append([nc.job_code,aud_sch.schedule_audit_code,nc.ncr_code,aud_sch.schedule_auditor_list.all(),
                        aud_sch.schedule_auditee_list.all(),ac.department.department_name,ac.cls_refno,ac.description,ac.auditor_comments,nc.root_cause_analysis,
                        nc.correction,nc.corrective_action,'',ncr_closed_date])

        lis1 = []
        for row in rows:
            lis2 = []
            for col_num in range(len(row)):
                lis2.append( '/ '.join([x.auditors.emp_name for x in row[col_num]])) if col_num == 3 else lis2.append('/ '.join([x.emp_name for x in row[col_num]])) if col_num == 4 else lis2.append(row[col_num])
            lis1.append(lis2[0::])
            lis2.clear()
        dic = {'details':lis1,'year':aud_yr}
        return render(self.request,'superadmin/ncr_report.html',dic )

    def export(request):
        # import form datas from above function using session
        aud_yr = request.session.get('audityear')
        aud_qua = request.session.get('auditquarter')
        a_type = request.session.get('auditype')

        response = HttpResponse(content_type='ms-excel')
        response['Content-Disposition'] = 'attachment; filename="ncr_report.xlsx"'
        wb = Workbook(response,{'default_date_format':'dd/mm/yy'})
        ws = wb.add_worksheet('NCR Report')
        date_time = 'Date',str(datetime.today().strftime('%d-%m-%Y'))
        date = ':'.join(date_time)
        merge_format1 = wb.add_format({
                        'border':1,
                        'align':'center',
                        'valign':'vcenter',
                        'text_wrap':True,
                        'bold':True})
        merge_format2 = wb.add_format({
                        'border':1,
                        'align':'center',
                        'valign':'vcenter',
                        'text_wrap':True,
                        })
        border_format = wb.add_format({'border':1})

        ws.merge_range("A1:N1",'4A DESIGN & ENGINEERING PVT LTD.',merge_format1)
        # (row,coloumn,width/height)
        ws.set_row(2,110)
        ws.set_column('A:A',6,border_format)
        ws.set_column('B:B',15,border_format)
        ws.set_column('C:C',7,border_format)
        ws.set_column('D:D',10,border_format)
        ws.set_column('E:E',18,border_format)
        ws.set_column('F:F',11,border_format)
        ws.set_column('G:G',5,border_format)
        ws.set_column('H:H',17,border_format)
        ws.set_column('I:I',22,border_format)
        ws.set_column('J:J',15,border_format)
        ws.set_column('K:K',15,border_format)
        ws.set_column('L:L',15,border_format)
        ws.set_column('M:M',12,border_format)
        ws.set_column('N:N',10,border_format)

        ws.merge_range("A2:D2",'Document No:4A:FRM:08',merge_format1)
        ws.merge_range("E2:F2","Issue:1",merge_format1)
        ws.merge_range("G2:K2",'INTERNAL AUDIT NCR/CAR FOR'+' '+aud_yr,merge_format1)
        ws.write(1,11,"Rev No:A",merge_format1)
        ws.merge_range("M2:N2",'Date:01.04.2014',merge_format1)
        ws.write(2,0,"Job No",merge_format1)
        ws.write(2,1,"Audit No",merge_format1)
        ws.write(2,2,"NCR/CAR No",merge_format1)
        ws.write(2,3,"Auditor",merge_format1)
        ws.write(2,4,"Auditee",merge_format1)
        ws.write(2,5,"Department",merge_format1)
        ws.write(2,6,"ISO Clause Ref No",merge_format1)
        ws.write(2,7,"Description",merge_format1)
        ws.write(2,8,"Observed Non - Conformance",merge_format1)
        ws.write(2,9,"Root Cause Analysis (What failed in the system to allow this non conformity to occur)",merge_format1)
        ws.write(2,10,"Correction (What is done to solve this problem)",merge_format1)
        ws.write(2,11,"Corrective action (What is done to prevent re-occarrence)",merge_format1)
        ws.write(2,12,"Implementation of Corrective Action",merge_format1)
        ws.write(2,13,"NCR Closed Date",merge_format1)

        rows = []
        nc_cmt_id = [i.id for i in Audit_comments.objects.all()]
        for nc in NCR_Comment.objects.all():
            if int(nc.command_id) in nc_cmt_id:
                aud_sch = Auditschedule.objects.get(pk=int(nc.audit_id))
                ac = Audit_comments.objects.get(pk=int(nc.command_id))
                ncr_closed_date = '' if nc.ncr_closed_on == None else str(nc.ncr_closed_on.date().strftime('%d-%m-%Y'))
                if ac.comment_status == 2:
                    spl = nc.ncr_code.split('-')
                    if (spl[2] == aud_qua and spl[1] == aud_yr and a_type==aud_sch.schedule_auditype.audittype) or (spl[2] == aud_qua and spl[1] == aud_yr and a_type==""):
                        rows.append([nc.job_code,aud_sch.schedule_audit_code,nc.ncr_code,aud_sch.schedule_auditor_list.all(),
                        aud_sch.schedule_auditee_list.all(),ac.department.department_name,ac.cls_refno,ac.description,ac.auditor_comments,nc.root_cause_analysis,
                        nc.correction,nc.corrective_action,'',ncr_closed_date])

        row_num = 2
        for row in rows:
            row_num += 1
            for col_num in range(len(row)):
                ws.write(row_num, col_num, '/ '.join([x.auditors.emp_name for x in row[col_num]]),merge_format2) if col_num == 3 else ws.write(row_num, col_num, '/ '.join([x.emp_name for x in row[col_num]]),merge_format2) if col_num == 4 else ws.write(row_num, col_num, row[col_num],merge_format2)

        wb.close()
        return response


class ProjectExportTable(FormView):
    form_class = ExportProjectForm
    template_name = 'superadmin/project_report_form.html'

    def post(self, request, *args, **kwargs):
        form = ExportProjectForm(request.POST)
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self,form):
        aud_yr = self.request.POST.get('audityear')
        pro_code = self.request.POST.get('project_code')
        a_type = self.request.POST.get('auditype')
        # export form data to another function using session
        self.request.session['audityear'] = self.request.POST['audityear']
        self.request.session['project_code'] = self.request.POST['project_code']
        self.request.session['auditype'] = self.request.POST['auditype']
        rows = []
        for asd in Auditschedule.objects.all().order_by('pk'):
            if asd.schedule_audit_code != None:
                spl = asd.schedule_audit_code.split('/')
                if (aud_yr == '' and asd.schedule_job_code == pro_code and a_type=='') or (spl[2] == aud_yr and asd.schedule_job_code == pro_code and a_type=='') or (spl[2] == aud_yr and asd.schedule_job_code == pro_code and a_type==asd.schedule_auditype.audittype):
                    if spl[1] == 'Q1':
                        rows.append([asd.schedule_job_code,'asd.schedule_project.project_name',"\n".join([asd.schedule_audit_code,asd.schedule_audit_date.strftime('%d-%m-%Y')]),'','',''])
                    elif spl[1] == 'Q2':
                        rows.append([asd.schedule_job_code,'asd.schedule_project.project_name','',"\n".join([asd.schedule_audit_code,asd.schedule_audit_date.strftime('%d-%m-%Y')]),'',''])
                    elif spl[1] == 'Q3':
                        rows.append([asd.schedule_job_code,'asd.schedule_project.project_name','','',"\n".join([asd.schedule_audit_code,asd.schedule_audit_date.strftime('%d-%m-%Y')]),''])
                    elif spl[1] == 'Q4':
                        rows.append([asd.schedule_job_code,'asd.schedule_project.project_name','','','',"\n".join([asd.schedule_audit_code,asd.schedule_audit_date.strftime('%d-%m-%Y')])])

        lis1 = []
        for row in rows:
            lis2 = []
            for col_num in range(len(row)):
                    lis2.append(row[col_num])
            lis1.append(lis2[0::])
            lis2.clear()
        dic = {'details':lis1}
        return render(self.request,'superadmin/project_report.html',dic )

    def export(request):
        # import form datas from above function using session
        aud_yr = request.session.get('audityear')
        pro_code = request.session.get('project_code')
        a_type = request.session.get('auditype')

        response = HttpResponse(content_type='ms-excel')
        response['Content-Disposition'] = 'attachment; filename="project_report.xlsx"'
        wb = Workbook(response,{'default_date_format':'dd/mm/yy'})
        ws = wb.add_worksheet('Project_Report')
        date_time = 'Date',str(datetime.today().strftime('%d-%m-%Y'))
        date = ':'.join(date_time)
        merge_format1 = wb.add_format({
                        'border':1,
                        'align':'center',
                        'valign':'vcenter',
                        'text_wrap':True,
                        'bold':True})
        merge_format2 = wb.add_format({
                        'border':1,
                        'align':'center',
                        'valign':'vcenter',
                        'text_wrap':True})
        border_format = wb.add_format({'border':1})

        ws.merge_range("A1:F1",'4A DESIGN & ENGINEERING PVT LTD.',merge_format1)
        ws.set_row(1,40)
        ws.set_column('A:A',20,border_format)
        ws.set_column('B:B',60,border_format)
        ws.set_column('C:C',20,border_format)
        ws.set_column('D:D',20,border_format)
        ws.set_column('E:E',20,border_format)
        ws.set_column('F:F',20,border_format)
        ws.write("A2",'Document No:',merge_format1)
        ws.write("B2","Issue:",merge_format1)
        ws.merge_range("C2:D2",'INTERNAL QUALITY AUDIT SCHEDULE FOR THE QUARTER',merge_format1)
        ws.write("E2","Rev No:",merge_format1)
        ws.write("F2",date,merge_format1)
        ws.write("A3","Project Code",merge_format1)
        ws.write("B3","Project Name",merge_format1)
        ws.write("C3","Q1",merge_format1)
        ws.write("D3","Q2",merge_format1)
        ws.write("E3","Q3",merge_format1)
        ws.write("F3","Q4",merge_format1)
        rows = []
        for asd in Auditschedule.objects.all().order_by('pk'):
            if asd.schedule_audit_code != None:
                spl = asd.schedule_audit_code.split('/')
                if (spl[2] == aud_yr and asd.schedule_job_code == pro_code and a_type=='') or (spl[2] == aud_yr and asd.schedule_job_code == pro_code and a_type==asd.schedule_auditype.audittype):
                    if spl[1] == 'Q1':
                        rows.append([asd.schedule_job_code,asd.schedule_project.project_name,"\n".join([asd.schedule_audit_code,asd.schedule_audit_date.strftime('%d-%m-%Y')]),'','',''])
                    elif spl[1] == 'Q2':
                        rows.append([asd.schedule_job_code,asd.schedule_project.project_name,'',"\n".join([asd.schedule_audit_code,asd.schedule_audit_date.strftime('%d-%m-%Y')]),'',''])
                    elif spl[1] == 'Q3':
                        rows.append([asd.schedule_job_code,asd.schedule_project.project_name,'','',"\n".join([asd.schedule_audit_code,asd.schedule_audit_date.strftime('%d-%m-%Y')]),''])
                    elif spl[1] == 'Q4':
                        rows.append([asd.schedule_job_code,asd.schedule_project.project_name,'','','',"\n".join([asd.schedule_audit_code,asd.schedule_audit_date.strftime('%d-%m-%Y')])])

        row_num = 2
        for row in rows:
            row_num += 1
            for col_num in range(len(row)):
                ws.write(row_num, col_num, row[col_num],merge_format2)
        wb.close()
        return response


class NCRLogExportTable(FormView):
    form_class = ExportForm
    template_name = 'superadmin/ncrlog_report_form.html'

    def post(self, request, *args, **kwargs):
        form = ExportForm(request.POST)
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self,form):
        aud_yr = self.request.POST.get('audityear')
        aud_qua = self.request.POST.get('auditquarter')
        a_type = self.request.POST.get('auditype')
        # export form data to another function using session
        self.request.session['audityear'] = self.request.POST['audityear']
        self.request.session['auditquarter'] = self.request.POST['auditquarter']
        self.request.session['auditype'] = self.request.POST['auditype']
        rows = []
        nc_cmt_id = [i.id for i in Audit_comments.objects.all()]
        for nc in NCR_Comment.objects.all():
            if nc.command_id in nc_cmt_id:
                aud_sch = Auditschedule.objects.get(pk=nc.audit_id)
                ac = Audit_comments.objects.get(pk=nc.command_id)
                ncr_closed_date = '' if nc.ncr_closed_on == None else str(nc.ncr_closed_on.date().strftime('%d-%m-%Y'))
                if ac.comment_status == 2:
                    spl = nc.ncr_code.split('-')
                    if (spl[2] == aud_qua and spl[1] == aud_yr and a_type == aud_sch.schedule_auditype.audittype) or (spl[2] == aud_qua and spl[1] == aud_yr and a_type == ''):
                        rows.append([nc.ncr_code,str(nc.create_on.date().strftime('%d-%m-%Y')),aud_sch.schedule_auditee_list.all(),
                        ac.cls_refno,aud_sch.schedule_auditor_list.all(),aud_sch.schedule_audit_date.strftime('%d-%m-%Y'),
                        aud_sch.schedule_audit_date.strftime('%d-%m-%Y'),ncr_closed_date,""])

        lis1 = []
        for row in rows:
            lis2 = []
            for col_num in range(len(row)):
                lis2.append( '/ '.join(['x.auditors.emp_name' for x in row[col_num]])) if col_num == 4 else lis2.append('/ '.join([x.emp_name for x in row[col_num]])) if col_num == 2 else lis2.append(row[col_num])
            lis1.append(lis2[0::])
            lis2.clear()
        dic = {'details':lis1}
        return render(self.request,'superadmin/ncrlog_report.html',dic )

    def export(request):
        # import form datas from above function using session
        aud_yr = request.session.get('audityear')
        aud_qua = request.session.get('auditquarter')
        a_type = request.session.get('auditype')

        response = HttpResponse(content_type='ms-excel')
        response['Content-Disposition'] = 'attachment; filename="ncrlog_report.xlsx"'
        wb = Workbook(response,{'default_date_format':'dd/mm/yy'})
        ws = wb.add_worksheet('NCR log Report')
        date_time = 'Date',str(datetime.today().strftime('%d-%m-%Y'))
        date = ':'.join(date_time)
        merge_format1 = wb.add_format({
                        'border':1,
                        'align':'center',
                        'valign':'vcenter',
                        'text_wrap':True,
                        'bold':True})
        merge_format2 = wb.add_format({
                        'border':1,
                        'align':'center',
                        'valign':'vcenter',
                        'text_wrap':True})
        border_format = wb.add_format({'border':1})

        ws.merge_range("A1:I1",'4A DESIGN & ENGINEERING PVT LTD.',merge_format1)
        # (row,coloumn,width/height)
        ws.set_row(2,40)
        ws.set_column('A:A',20,border_format)
        ws.set_column('B:B',15,border_format)
        ws.set_column('C:C',35,border_format)
        ws.set_column('D:D',15,border_format)
        ws.set_column('E:E',20,border_format)
        ws.set_column('F:F',15,border_format)
        ws.set_column('G:G',15,border_format)
        ws.set_column('H:H',15,border_format)
        ws.set_column('I:I',18,border_format)
        ws.merge_range("A2:C2",'Document No:4A:FRM:08',merge_format1)
        ws.merge_range("D2:E2","Issue:1",merge_format1)
        ws.merge_range("F2:G2","Rev No:A",merge_format1)
        ws.merge_range("H2:I2","Date:01.04.2014",merge_format1)
        ws.write(2,0,"NCR",merge_format1)
        ws.write(2,1,"NCR Date",merge_format1)
        ws.write(2,2,"NCR Issued To",merge_format1)
        ws.write(2,3,"Non Conformity ISO CL.NO.",merge_format1)
        ws.write(2,4,"Initiator",merge_format1)
        ws.write(2,5,"Date to complete",merge_format1)
        ws.write(2,6,"Date Completed",merge_format1)
        ws.write(2,7,"NCR Closed Date",merge_format1)
        ws.write(2,8,"Remarks",merge_format1)

        rows = []
        nc_cmt_id = [i.id for i in Audit_comments.objects.all()]
        for nc in NCR_Comment.objects.all():
            if int(nc.command_id) in nc_cmt_id:
                aud_sch = Auditschedule.objects.get(pk=int(nc.audit_id))
                ac = Audit_comments.objects.get(pk=int(nc.command_id))
                ncr_closed_date = '' if nc.ncr_closed_on == None else str(nc.ncr_closed_on.date().strftime('%d-%m-%Y'))
                if ac.comment_status == 2:
                    spl = nc.ncr_code.split('-')
                    if (spl[2] == aud_qua and spl[1] == aud_yr and a_type == aud_sch.schedule_auditype.audittype) or (spl[2] == aud_qua and spl[1] == aud_yr and a_type == ''):
                        rows.append([nc.ncr_code,str(nc.create_on.date().strftime('%d-%m-%Y')),aud_sch.schedule_auditee_list.all(),
                        ac.cls_refno,aud_sch.schedule_auditor_list.all(),aud_sch.schedule_audit_date.strftime('%d-%m-%Y'),
                        aud_sch.schedule_audit_date.strftime('%d-%m-%Y'),ncr_closed_date,""])

        row_num = 2
        for row in rows:
            row_num += 1
            for col_num in range(len(row)):
                ws.write(row_num, col_num, '/ '.join([x.auditors.emp_name for x in row[col_num]]),merge_format2) if col_num == 4 else ws.write(row_num, col_num, '/ '.join([x.emp_name for x in row[col_num]]),merge_format2) if col_num == 2 else ws.write(row_num, col_num, row[col_num],merge_format2)
        wb.close()
        return response




#
# class AuditscheduleConfirming(View):
#     model = Auditschedule
#     success_url = 'QMS:auditscheduleview'
#
#     def get_success_url(self):
#         return reverse_lazy(self.success_url)
#
#     def get(self, request, *args, **kwargs):
#         auditschedule = self.model.objects.get(pk=self.kwargs.get("pk"))
#         Q1 = ['01','02','03']
#         Q2 = ['04','05','06']
#         Q3 = ['07','08','09']
#         Q4 = ['10','11','12']
#         ac = []
#         # auditees = auditschedule.schedule_auditee_list.emp_name
#         auditype = auditschedule.schedule_auditype.auditcode
#         ad = auditschedule.schedule_audit_date
#         auditdate = str(ad).split('-')
#         ac.append(auditype)
#         if auditdate[1] in Q1:
#             ac.append('Q1')
#         elif auditdate[1] in Q2:
#             ac.append('Q2')
#         elif auditdate[1] in Q3:
#             ac.append('Q3')
#         elif auditdate[1] in Q4:
#             ac.append('Q4')
#         ac.append(auditdate[0])
#         ac.append(str(auditschedule.id))
#         auditcode = '/'.join(ac)
#         auditschedule.schedule_audit_code = auditcode
#
#         auditschedule.save()
#         return HttpResponseRedirect(self.get_success_url())
#
