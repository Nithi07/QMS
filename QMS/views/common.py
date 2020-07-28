from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from QMS.models import Audittype, EmployePosition, EmployeDepartment
from QMS.form.formcommon import Audittypeform, EmployePositionform, EmployeDepartmentform
from django.views.generic import ListView, DetailView, TemplateView, CreateView, UpdateView, DeleteView
from django.urls import  reverse_lazy

#Audittype TemplateView
class HomePage(TemplateView):
    template_name = 'superadmin/home.html'

#Audittype ListView
class AudittypeListview(ListView):
    model = Audittype
    template_name = 'superadmin/audittype_view.html'

    def get_context_data(self, **kwargs):
        listaudittype = self.model.objects.all().order_by('pk')
        obj = {'listaudittype':listaudittype}
        return obj

#Audittype CreateView
class AudittypeCreate(CreateView):
    model = Audittype
    form_class = Audittypeform
    success_url = 'QMS:audittypeview'
    template_name = 'superadmin/audittype.html'

    # def get_context_data(self, **kwargs):
    #     context = super(AudittypeCreate, self).get_context_data(**kwargs)
    #     context['audittype'] = 'test'
    #     return context

    def get_initial(self):
        self.initial = {'audittype':'test'}
        return self.initial

    def get_success_url(self):
       return reverse_lazy(self.success_url)


    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        create_by="admin"
        create_ip="192.168.2.14"
        form.save()
        return HttpResponseRedirect(self.get_success_url())

#Audittype UpdateView
class AudittypeUpdate(UpdateView):
     model = Audittype
     form_class = Audittypeform
     success_url = 'QMS:audittypeview'
     template_name = 'superadmin/audittype.html'

     def get_success_url(self):
        return reverse_lazy(self.success_url)

     def form_valid(self, form):
         form.save()
         return HttpResponseRedirect(self.get_success_url())

#Audittype DeleteView
class AudittypeDelete(DeleteView):
    model = Audittype
    success_url = 'QMS:audittypeview'
    template_name = 'superadmin/audittype_confirm_delete.html'

    def get_object(self, queryset=None):
        """ Hook to ensure object is owned by request.user. """
        obj = super(AudittypeDelete, self).get_object()
        return obj
    def get_success_url(self):
        return reverse_lazy(self.success_url)

#EmployePosition ListView
class EmployePositionListview(ListView):
    model = EmployePosition
    template_name = 'superadmin/empposition_view.html'

    def get_context_data(self, **kwargs):
        empposition = self.model.objects.all().order_by('pk')
        obj = {'empposition':empposition}
        return obj

#EmployePosition CreateView
class EmployePositionCreate(CreateView):
    model = EmployePosition
    form_class = EmployePositionform
    success_url = 'QMS:emppositionview'
    template_name = 'superadmin/empposition_form.html'

    def get_success_url(self):
       return reverse_lazy(self.success_url)

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        form.save()
        return HttpResponseRedirect(self.get_success_url())


#EmployePosition UpdateView
class EmployePositionUpdate(UpdateView):
     model = EmployePosition
     form_class = EmployePositionform
     success_url = 'QMS:emppositionview'
     template_name = 'superadmin/empposition_form.html'

     def get_success_url(self):
        return reverse_lazy(self.success_url)

     def form_valid(self, form):
        form = self.get_form()
        form.save()
        return HttpResponseRedirect(self.get_success_url())


#EmployePosition DeleteView
class EmployePositionDelete(DeleteView):
    model = EmployePosition
    success_url = 'QMS:emppositionview'
    template_name = 'superadmin/empposition_confirm_delete.html'

    def get_object(self, queryset=None):
        """ Hook to ensure object is owned by request.user. """
        obj = super(EmployePositionDelete, self).get_object()
        return obj
    def get_success_url(self):
        return reverse_lazy(self.success_url)


#EmployeDepartment ListView
class EmployeDepartmentListview(ListView):
    model = EmployeDepartment
    template_name = 'superadmin/empdept_view.html'

    def get_context_data(self, **kwargs):
        listdept = self.model.objects.all().order_by('pk')
        obj = {'listdept':listdept}
        return obj

#EmployeDepartment CreateView
class EmployeDepartmentCreate(CreateView):
    model = EmployeDepartment
    form_class = EmployeDepartmentform
    success_url = 'QMS:employedeptview'
    template_name = 'superadmin/empdept_form.html'

    def get_success_url(self):
       return reverse_lazy(self.success_url)

    def get_context_data(self, **kwargs):
        context = super(EmployeDepartmentCreate, self).get_context_data(**kwargs)
        context['form'] = EmployeDepartmentform()
        return context

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        form.save()
        return HttpResponseRedirect(self.get_success_url())

#EmployeDepartment UpdateView
class EmployeDepartmentUpdate(UpdateView):
     model = EmployeDepartment
     form_class = EmployeDepartmentform
     success_url = 'QMS:employedeptview'
     template_name = 'superadmin/empdept_form.html'

     def get_success_url(self):
        return reverse_lazy(self.success_url)
     def form_valid(self, form):
        form = self.get_form()
        form.save()
        return HttpResponseRedirect(self.get_success_url())

#EmployeDepartment DeleteView
class EmployeDepartmentDelete(DeleteView):
    model = EmployeDepartment
    success_url = 'QMS:employedeptview'
    template_name = 'superadmin/empdept_confirm_delete.html'

    def get_object(self, queryset=None):
        """ Hook to ensure object is owned by request.user. """
        obj = super(EmployeDepartmentDelete, self).get_object()
        return obj

    def get_success_url(self):
        return reverse_lazy(self.success_url)
