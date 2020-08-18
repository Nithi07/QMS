from django.shortcuts import render, redirect
from django.db import transaction
from django.http import HttpResponse, HttpResponseRedirect
from QMS.models import Auditschedule
from QMS.models import Audittype,EmployeDepartment
from QMS.models import WorkManual
from QMS.models import ManualCheckList
from QMS.models import Audit_comments
from QMS.models import NCR_Comment
from QMS.views.mailgenerate import Mail
from QMS.form.auditcommentform import mr_commentsForm,Auditee_commentsForm,Verified_commentsForm,NCR_commentsForm
from QMS.form.auditcommentform import Auditor_commentsForm,Auditor_commentsFormset
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import  reverse_lazy
from django.db.models import Q
from django.contrib import messages
from datetime import datetime
from django.forms import inlineformset_factory,modelformset_factory
from Timesheet.settings import EMAIL_HOST_USER
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.core.mail import send_mail,EmailMultiAlternatives,EmailMessage


def load_page(request):
    ac = Audit_comments.objects.get(id=request.GET.get('auditcomments_id'))
    nc = NCR_Comment.objects.get(id=request.GET.get('ncrcomments_id'))
    auditschedule = Auditschedule.objects.get(pk=ac.auditschedule_id)
    wkm = []
    for i in WorkManual.objects.all():
        for j in i.audit_typ.filter(audittype=auditschedule.schedule_auditype.audittype):
            wkm.append(i)
    return render(request, 'superadmin/verify_ajax.html',{'ac':ac,'workmanual':wkm,'nc':nc,'auditschedule':auditschedule})


class MrcommentListCreate(ListView):
    model = Audit_comments
    form_class = mr_commentsForm
    template_name = 'superadmin/auditorcomment_view.html'
    success_url = 'QMS:auditscheduleview'

    def get_context_data(self, **kwargs):
        context = super(MrcommentListCreate, self).get_context_data(**kwargs)
        context['form'] = mr_commentsForm()
        auditorcomments = Audit_comments.objects.filter(auditschedule=self.kwargs.get("pk")).order_by('pk')
        context["auditorcomments"] = auditorcomments
        status_satisfied = 0
        if auditorcomments.count() == len([i.mr_status for i in auditorcomments if i.mr_status == 2]):
            status_satisfied += 1
        context["auditschedule"] = Auditschedule.objects.get(pk=self.kwargs.get("pk"))
        context["ncrcomments"] = NCR_Comment.objects.filter(audit_id=self.kwargs.get("pk")).order_by('pk')
        context['status_satisfied'] = status_satisfied
        return context

    def get_success_url(self):
       return reverse_lazy(self.success_url)

    def post(self, request, *args, **kwargs):
        if request.method == 'POST':
            form = mr_commentsForm(request.POST)
            if form.is_valid():
                return self.form_valid(form,request)
            else:
                return self.form_invalid(form)

    def form_valid(self,form,request):
        id = request.POST.getlist('id')
        mr_com = request.POST.getlist('mr_comments')
        mr_sts = request.POST.getlist('mr_status')
        c = len(id)

        for k in range(c):
             if int(mr_sts[k]) != 2:
                verified_status=1
                auditee_status=0
                audit_comment_status = 1
             else:
                 verified_status=2
                 auditee_status=1
                 audit_comment_status = 6
             Audit_comments.objects.filter(pk=id[k]).update(mr_comments = mr_com[k],mr_status = mr_sts[k],verified_status=verified_status,auditee_status=auditee_status)
             Auditschedule.objects.filter(pk=self.kwargs.get("pk")).update(audit_comment_status = audit_comment_status)
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

    def Sendmail(request,id):
        subject = 'MR Report'
        message = 'Received your Reports'
        mr_status = [i.mr_status for i in Audit_comments.objects.filter(auditschedule=id)]
        to,cc = [],[]
        html_content = render_to_string('superadmin/',{'mail':1})
        plain_message = strip_tags(html_content)
        if (0 not in mr_status) and (1 not in mr_status):
            Auditschedule.objects.filter(pk=id).update(audit_comment_status = 6)
        if len(to) == 0:
            messages.success(request, 'Mail Send Failed \U0001F44E \U0001F44E \U0001F44E')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        else:
            return Mail.mailgenerate(request,subject,plain_message,EMAIL_HOST_USER,to,cc,html_content)


class AuditorcommentCreate(CreateView):
    model = Audit_comments
    form_class = Auditor_commentsForm
    template_name = 'superadmin/auditorcomment_form.html'
    success_url = 'QMS:auditscheduleview'

    def get_context_data(self, **kwargs):
        context = super(AuditorcommentCreate, self).get_context_data(**kwargs)
        auditschedule = Auditschedule.objects.get(pk=self.kwargs.get("pk"))
        wkm = []
        for i in WorkManual.objects.filter(project_type__contains=['Project']).order_by('pk'):
            for j in i.audit_typ.filter(audittype=auditschedule.schedule_auditype.audittype):
                # if j.audittype == auditschedule.schedule_auditype.audittype:
                wkm.append(i)
        context["form"]=Auditor_commentsForm()
        Auditor_commentsFormset = modelformset_factory(Audit_comments,form=Auditor_commentsForm,extra=0)
        context["formset"] = Auditor_commentsFormset(queryset=Audit_comments.objects.filter(auditschedule=auditschedule))
        context["auditschedule"] = auditschedule
        context["acid"] = [i.auditschedule_id for i in Audit_comments.objects.filter(auditschedule=auditschedule)]
        context["workmanual"] = wkm
        context["employeedept"] = EmployeDepartment.objects.filter(Q(dept_code='CVL')|Q(dept_code='MECH')|Q(dept_code='ELE')|Q(dept_code='TL'))
        return context


    def get_success_url(self):
       return reverse_lazy(self.success_url)


    def post(self, request, *args, **kwargs):
        form=Auditor_commentsForm(request.POST)
        Auditor_commentsFormset = modelformset_factory(Audit_comments,form=Auditor_commentsForm,extra=0)
        formset = Auditor_commentsFormset(request.POST)

        if form.is_valid():
            return self.form_valid(form,request)
        else:
            messages.error(request,"Failed")

        if formset.is_valid():
            return self.formset_valid(formset,request)
        else:
            messages.error(request,"Failed")

    def form_valid(self,form,request):
        # print(form.cleaned_data.get('auditor_comments'))
        print(form.cleaned_data['auditor_comments'])
        # for i in form:
        #     cd = i.cleaned_data
        #     print(cd.getlist('auditor_comments'))
        # print(request.POST.getlist('auditor_comments'))

        Auditschedule.objects.filter(pk=self.kwargs.get("pk")).update(audit_comment_status=2)
        aud_cmt = request.POST.getlist('auditor_comments')
        cls_no = request.POST.getlist('cls_refno')
        desc = request.POST.getlist('description')
        aud_sts = request.POST.getlist('comment_status')
        dept = request.POST.getlist('department')
        wm_id = request.POST.getlist('workmanual')
        as_id = Auditschedule.objects.get(pk=self.kwargs.get("pk"))
        lenth =  request.POST['totallength']
        if lenth != '':
            for index in range(int(lenth)):
                Audit_comments.objects.create(cls_refno=request.POST['cls_refno'+str(index)],description=request.POST['description'+str(index)],
                                   auditor_comments=request.POST['auditor_comments'+str(index)],comment_status=request.POST['comment_status'+str(index)],department=EmployeDepartment.objects.get(id=request.POST['department'+str(index)]),
                                   auditschedule = Auditschedule.objects.get(pk=self.kwargs.get("pk")),create_by='admin',create_ip='192.168.2.14',create_on=datetime.today())

        c = len(wm_id)
        for i in range(c):
            if dept[i] == '':
                department = None
            else:
                department = EmployeDepartment.objects.get(id=int(dept[i]))
            # print(form.cleaned_data.getlist('cls_refno'))
            Audit_comments.objects.create(cls_refno=cls_no[i],description=desc[i],
                               auditor_comments=aud_cmt[i],comment_status=aud_sts[i],department=department,
                               auditschedule = Auditschedule.objects.get(pk=self.kwargs.get("pk")),workmanual=WorkManual.objects.get(id=int(wm_id[i])),create_by='admin',create_ip='192.168.2.14',create_on=datetime.today())

        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


    def formset_valid(self,formset,request):
        import pdb; pdb.set_trace()
        lenth =  request.POST['totallength']
        if lenth != '':
            for index in range(int(lenth)):
                Audit_comments.objects.create(cls_refno=request.POST['cls_refno'+str(index)],description=request.POST['description'+str(index)],
                                   auditor_comments=request.POST['auditor_comments'+str(index)],comment_status=request.POST['comment_status'+str(index)],department=EmployeDepartment.objects.get(id=request.POST['department'+str(index)]),
                                   auditschedule = Auditschedule.objects.get(pk=self.kwargs.get("pk")),create_by='admin',create_ip='192.168.2.14',create_on=datetime.today())

        for f in formset:
            cd = f.cleaned_data
            obj = cd.get('id')
            Audit_comments.objects.filter(pk=obj.id).update(auditor_comments=cd.get('auditor_comments'),
                                    comment_status=cd.get('comment_status'),department=cd.get('department'))

        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))



    def Sendmail(request,id):
        subject = 'Comment Report'
        Auditschedule.objects.filter(pk=id).update(audit_comment_status = 3)
        to,cc = [],[]
        html_content = render_to_string('',{'mail':1})
        plain_message = 'Received your Reports'
        if len(to) == 0:
            messages.success(request, 'Mail Send Failed \U0001F44E \U0001F44E \U0001F44E')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        else:
            return Mail.mailgenerate(request,subject,plain_message,EMAIL_HOST_USER,to,cc,html_content)



class AuditeecommentCreate(CreateView):
    model = Audit_comments
    form_class = Auditee_commentsForm
    template_name = 'superadmin/auditeecomment_form.html'
    success_url = 'QMS:auditscheduleview'

    def get_success_url(self):
       return reverse_lazy(self.success_url)

    def get_context_data(self, **kwargs):
        context = super(AuditeecommentCreate, self).get_context_data(**kwargs)
        auditcomments = Audit_comments.objects.filter(auditschedule=self.kwargs.get("pk")).order_by('pk')
        context["auditschedule"] = Auditschedule.objects.get(pk=self.kwargs.get("pk"))
        context["auditcomments"] = auditcomments
        status_satisfied = 0
        if auditcomments.count() == len([i.auditee_status for i in auditcomments if i.auditee_status == 1]):
            status_satisfied += 1
        context["form1"] = Auditee_commentsForm()
        context["form2"] = NCR_commentsForm()
        context["ncrcommentid"] = [i.command_id for i in NCR_Comment.objects.filter(audit_id=self.kwargs.get("pk"))]
        context["ncrcomments"] = NCR_Comment.objects.filter(audit_id=self.kwargs.get("pk")).order_by('pk')
        context['status_satisfied'] = status_satisfied
        return context

    def post(self, request, *args, **kwargs):
        form1 = Auditee_commentsForm(request.POST)
        form2 = NCR_commentsForm(request.POST)
        if form1.is_valid() or form2.is_valid():
            return self.form_valid(form1,form2,request)

    def form_valid(self,form1,form2,request):
        auditschedule = Auditschedule.objects.get(pk=self.kwargs.get("pk"))
        Auditschedule.objects.filter(pk=self.kwargs.get("pk")).update(audit_comment_status = 3)
        if form1.is_valid():
            id = request.POST.getlist('id')
            aude_com = request.POST.getlist('auditee_correction')
            aude_sts = request.POST.getlist('auditee_status')
            for k in range(len(id)):
                Audit_comments.objects.filter(pk=int(id[k])).update(auditee_correction = aude_com[k],auditee_status = int(aude_sts[k]))
        if form2.is_valid():
            with_ncr_commentid = request.POST.getlist('with_ncr_commentid')
            ncr_id = request.POST.getlist('ncr_id')
            root_cau = request.POST.getlist('root_cause_analysis')
            corr = request.POST.getlist('correction')
            corr_action = request.POST.getlist('corrective_action')
            aude_sts = request.POST.getlist('auditee_status_ncr')

            exi_ncr_id = [i.command_id for i in NCR_Comment.objects.filter(audit_id=self.kwargs.get("pk"))]
            asss = str(auditschedule.schedule_audit_code)

            ncr_count = 0
            if NCR_Comment.objects.all().count() == 0:
                ncr_count += 0
            else:
                ncr_count += NCR_Comment.objects.latest('id').id
            for o in range(len(with_ncr_commentid)):
                as_spl = asss.split('/')
                ncr_code = ['ncr',as_spl[2],as_spl[1],str(ncr_count)]
                ncr_count += 1
                Audit_comments.objects.filter(pk=with_ncr_commentid[o]).update(auditee_correction = corr_action[o],auditee_status=aude_sts[o])
                if int(with_ncr_commentid[o]) in exi_ncr_id:
                    NCR_Comment.objects.filter(pk=ncr_id[o]).update(job_code = auditschedule.schedule_job_code,root_cause_analysis = root_cau[o],correction = corr[o],
                                corrective_action = corr_action[o],audit_id = auditschedule.id, command_id = with_ncr_commentid[o])
                else:
                    NCR_Comment.objects.create(ncr_code = '-'.join(ncr_code),job_code = auditschedule.schedule_job_code,root_cause_analysis = root_cau[o],correction = corr[o],
                            corrective_action = corr_action[o],audit_id = auditschedule.id, command_id = with_ncr_commentid[o],create_by='admin',create_ip='192.168.2.14',create_on=datetime.today())

        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

    def Sendmail(request,id):
        subject = 'Auditee Report'
        auditee_status = [i.auditee_status for i in Audit_comments.objects.filter(auditschedule=id)]
        if 0 not in auditee_status:
            Auditschedule.objects.filter(pk=id).update(audit_comment_status = 4)
        to,cc = [],[]
        html_content = render_to_string('',{'mail':1})
        plain_message = 'Received your Reports'
        if len(to) == 0:
            messages.success(request, 'Mail Send Failed \U0001F44E \U0001F44E \U0001F44E')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        else:
            return Mail.mailgenerate(request,subject,plain_message,EMAIL_HOST_USER,to,cc,html_content)


class VerifycommentCreate(CreateView):
    model = Audit_comments
    form_class = Verified_commentsForm
    template_name = 'superadmin/verifycomment_form.html'
    success_url = 'QMS:auditscheduleview'

    def get_context_data(self, **kwargs):
        context = super(VerifycommentCreate, self).get_context_data(**kwargs)
        auditcomments = Audit_comments.objects.filter(auditschedule=self.kwargs.get("pk")).order_by('pk')
        status_satisfied = 0
        if auditcomments.count() == len([i.verified_status for i in auditcomments if i.verified_status == 2]):
            status_satisfied += 1
        context["auditschedule"] = Auditschedule.objects.get(pk=self.kwargs.get("pk"))
        context["auditcomments"] = auditcomments
        context["ncrcomments"] = NCR_Comment.objects.filter(audit_id=self.kwargs.get("pk")).order_by('pk')
        context['status_satisfied'] = status_satisfied
        return context

    def get_success_url(self):
       return reverse_lazy(self.success_url)

    def post(self, request, *args, **kwargs):
        form = Verified_commentsForm(request.POST)

        if form.is_valid():
            return self.form_valid(form,request)
        else:
            return self.form_invalid(form)

    def form_valid(self,form,request):
        Auditschedule.objects.filter(pk=self.kwargs.get("pk")).update(audit_comment_status = 4)
        id = request.POST.getlist('id')
        aude_com = request.POST.getlist('verified_comments')
        aude_sts = request.POST.getlist('verified_status')
        c = len(id)
        for k in range(c):
            Audit_comments.objects.filter(pk=id[k]).update(verified_comments = aude_com[k],verified_status = aude_sts[k])
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

    def Sendmail(request,id):
        subject = 'Verify Report'
        aude_sts = [i.verified_status for i in Audit_comments.objects.filter(auditschedule=id)]
        if (0 not in aude_sts) and (1 not in aude_sts):
            Auditschedule.objects.filter(pk=id).update(audit_comment_status = 5)
        to,cc = [],[]
        html_content = render_to_string('',{'mail':1})
        plain_message = 'Received your Reports'
        if len(to) == 0:
            messages.success(request, 'Mail Send Failed \U0001F44E \U0001F44E \U0001F44E')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        else:
            return Mail.mailgenerate(request,subject,plain_message,EMAIL_HOST_USER,to,cc,html_content)



# class MrcommentListUpdate(UpdateView):
#      model = Audit_comments
#      form_class = mr_commentsForm
#      success_url = 'QMS:auditorcommentview'
#      template_name = 'superadmin/mrcommet_update.html'
#
#      def get_context_data(self, **kwargs):
#              context = super(MrcommentListUpdate, self).get_context_data(**kwargs)
#              context["auditcomments"] = Audit_comments.objects.get(pk=self.kwargs.get("pk"))
#              return context
#
#      def get_success_url(self):
#         return reverse_lazy(self.success_url)
#
#      def post(self, request, *args, **kwargs):
#          form = mr_commentsForm(request.POST)
#          if form.is_valid():
#              return self.form_valid(form)
#          else:
#              return self.form_invalid(form)
#
#      def form_valid(self, form):
#
#          Audit_comments.objects.filter(pk=self.kwargs.get("pk")).update(
#          mr_comments = request.POST.get('mr_comments'),
#          mr_status = request.POST.get('mr_status'),
#          )
#          return redirect(request.META['HTTP_REFERER'])
#

# class AuditorcommentUpdate(CreateView):
#      model = Audit_comments
#      form_class = Auditor_commentsForm
#      success_url = 'QMS:auditscheduleview'
#      template_name = 'superadmin/auditorcomment_form.html'
#
#      def get_context_data(self, **kwargs):
#              context = super(AuditorcommentUpdate, self).get_context_data(**kwargs)
#              ashle = Auditschedule.objects.get(pk=self.kwargs.get("pk"))
#              # context["auditorcomments"] = Audit_comments.objects.get(pk=self.kwargs.get("pk"))
#              Auditor_commentsFormset = modelformset_factory(Audit_comments,form=Auditor_commentsForm,extra=0)
#              context["formset"] = Auditor_commentsFormset(queryset=Audit_comments.objects.filter(auditschedule_id=self.kwargs.get("pk")))
#              context["auditschedule"] = ashle
#              context["acid"] = [i.auditschedule_id_id for i in Audit_comments.objects.filter(auditschedule_id=self.kwargs.get("pk"))]
#              return context
#
#      def get_success_url(self):
#         return reverse_lazy(self.success_url)
#
#      def post(self, request, *args, **kwargs):
#          form=Auditor_commentsForm(request.POST)
#          Auditor_commentsFormset = modelformset_factory(Audit_comments,form=Auditor_commentsForm,extra=0)
#          formset = Auditor_commentsFormset(request.POST)
#          if formset.is_valid():
#              for f in formset:
#                  cd = f.cleaned_data
#                  obj = cd.get('id')
#                  Audit_comments.objects.filter(pk=obj.id).update(auditor_comments=cd.get('auditor_comments'),
#                                         comment_status=cd.get('comment_status'),department=cd.get('department'))
#          else:
#              messages.error(request,"Failed")
#          return HttpResponseRedirect(self.get_success_url())

     # def post(self, request, *args, **kwargs):
     #     form = Auditor_commentsForm(request.POST)
     #     if form.is_valid():
     #         Audit_comments.objects.filter(pk=self.kwargs.get("pk")).update(
     #         auditor_comments = request.POST.get('auditor_comments'),
     #         comment_status = request.POST.get('comment_status'),
     #         department = request.POST.get('department'),
     #         auditee_comments = request.POST.get('auditee_comments'),
     #         auditee_status = request.POST.get('auditee_status')
     #         )
     #     return HttpResponseRedirect(self.get_success_url())
     #



#
# class AuditeecommentUpdate(UpdateView):
#      model = Audit_comments
#      form_class = Auditee_commentsForm
#      success_url = 'QMS:auditscheduleview'
#      template_name = 'superadmin/auditeecomment_update.html'
#
#      def get_context_data(self, **kwargs):
#              context = super(AuditeecommentUpdate, self).get_context_data(**kwargs)
#              context["auditcomments"] = Audit_comments.objects.get(pk=self.kwargs.get("pk"))
#              context["ncrcomments"] = NCR_Comment.objects.all().order_by('pk')
#              return context
#
#      def get_success_url(self):
#         return reverse_lazy(self.success_url)
#
#
#      def post(self, request, *args, **kwargs):
#          form1 = Auditee_commentsForm(request.POST)
#          form2 = NCR_commentsForm(request.POST)
#
#          if form1.is_valid():
#              Audit_comments.objects.filter(pk=self.kwargs.get("pk")).update(
#              auditee_comments = request.POST.get('auditee_comments'),
#              auditee_status = request.POST.get('auditee_status'),
#              )
#          if form2.is_valid():
#              NCR_Comment.objects.filter(pk=request.POST.get('ncr_id')).update(
#              root_cause_analysis = request.POST.get('root_cause_analysis'),
#              correction = request.POST.get('correction'),
#              corrective_action = request.POST.get('corrective_action')
#              )
#          return HttpResponseRedirect(self.get_success_url())



#
# class VerifycommentUpdate(CreateView):
#
#      model = Audit_comments
#      form_class = Verified_commentsForm
#      success_url = 'QMS:auditscheduleview'
#      template_name = 'superadmin/verifycomment_update.html'
#
#      def get_context_data(self, **kwargs):
#              context = super(VerifycommentUpdate, self).get_context_data(**kwargs)
#              # context["auditcomments"] = Audit_comments.objects.get(pk=self.kwargs.get("pk"))
#              # context["ncrcomments"] = NCR_Comment.objects.all().order_by('pk')
#              context["auditschedule"] = Auditschedule.objects.get(pk=self.kwargs.get("pk"))
#              Auditor_commentsFormset = modelformset_factory(Audit_comments,form=Verified_commentsForm,extra=0)
#              context["formset"] = Auditor_commentsFormset(queryset=Audit_comments.objects.filter(auditschedule_id=self.kwargs.get("pk")))
#              return context
#
#      def get_success_url(self):
#         return reverse_lazy(self.success_url)
#
#      def post(self, request, *args, **kwargs):
#          form=Verified_commentsForm(request.POST)
#          Auditor_commentsFormset = modelformset_factory(Audit_comments,form=Verified_commentsForm,extra=0)
#          formset = Auditor_commentsFormset(request.POST)
#          if formset.is_valid():
#              for f in formset:
#                  cd = f.cleaned_data
#                  obj = cd.get('id')
#                  Audit_comments.objects.filter(pk=obj.id).update(verified_comments=cd.get('verified_comments'),
#                                         verified_status=cd.get('verified_status'))
#          else:
#              messages.error(request,"Failed")
#          return HttpResponseRedirect(self.get_success_url())

     # def post(self, request, *args, **kwargs):
     #     form = Verified_commentsForm(request.POST)
     #     if form.is_valid():
     #         Audit_comments.objects.filter(pk=self.kwargs.get("pk")).update(
     #         verified_comments = request.POST.get('verified_comments'),
     #         verified_status = request.POST.get('verified_status'),
     #         )
     #     return HttpResponseRedirect(self.get_success_url())
