from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from QMS.models import ListAuditors
from QMS.form.auditorlistform import Auditorlistform
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import  reverse_lazy


class AuditorlistListview(ListView):
    model = ListAuditors
    template_name = 'superadmin/auditorlist_view.html'

    def get_context_data(self, **kwargs):
        auditorlist = self.model.objects.all().order_by('pk')
        obj = {'auditorlist':auditorlist}
        return obj

#Auditorlist CreateView
class AuditorlistCreate(CreateView):
    model = ListAuditors
    form_class = Auditorlistform
    success_url = 'QMS:auditorlistview'
    template_name = 'superadmin/auditorlist_form.html'

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


class AuditorlistUpdate(UpdateView):
     model = ListAuditors
     form_class = Auditorlistform
     success_url = 'QMS:auditorlistview'
     template_name = 'superadmin/auditorlist_form.html'

     def get_success_url(self):
        return reverse_lazy(self.success_url)

     def form_valid(self, form):
        form = self.get_form()
        form.save()
        return HttpResponseRedirect(self.get_success_url())


#Auditorlist DeleteView
class AuditorlistDelete(DeleteView):
    model = ListAuditors
    success_url = 'QMS:auditorlistview'
    template_name = 'superadmin/auditorlist_confirm_delete.html'

    def get_object(self, queryset=None):
        """ Hook to ensure object is owned by request.user. """
        obj = super(AuditorlistDelete, self).get_object()
        return obj
        
    def get_success_url(self):
        return reverse_lazy(self.success_url)
