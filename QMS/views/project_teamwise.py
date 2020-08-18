from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from QMS.models import Project_Details
from QMS.models import Teamwise
from QMS.form.project_teamwiseform import Project_Detailsform,Teamwiseform
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView,View,FormView
from django.urls import  reverse_lazy
from django.contrib import messages
from datetime import datetime

class ProjectListview(ListView):
    model = Project_Details
    template_name = 'superadmin/project_view.html'
    def get_context_data(self, **kwargs):
        context = super(ProjectListview, self).get_context_data(**kwargs)
        context["projectdata"] = Project_Details.objects.all()
        return context


class ProjectCreate(CreateView):
    model = Project_Details
    form_class = Project_Detailsform
    template_name = 'superadmin/project_form.html'
    success_url = 'QMS:projectview'

    def get_success_url(self):
        return reverse_lazy(self.success_url)

    def post(self, request, *args, **kwargs):
        form = Project_Detailsform(request.POST)
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        form.save()
        return HttpResponseRedirect(self.get_success_url())


class ProjectUpdate(UpdateView):
    model = Project_Details
    form_class = Project_Detailsform
    template_name = 'superadmin/project_form.html'
    success_url = 'QMS:projectview'

    def get_success_url(self):
        return reverse_lazy(self.success_url)

    def form_valid(self, form):
        form = self.get_form()
        form.save()
        return HttpResponseRedirect(self.get_success_url())


class ProjectDelete(DeleteView):
     def ObjectDelete(request,pk):
         object=Project_Details.objects.get(id=pk)
         object.delete()
         return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


class TeamwiseListview(ListView):
    model = Teamwise
    template_name = 'superadmin/teamwise_view.html'
    def get_context_data(self, **kwargs):
        context = super(TeamwiseListview, self).get_context_data(**kwargs)
        context["teamwisedata"] = Teamwise.objects.all()
        return context


class TeamwiseCreate(CreateView):
    model = Teamwise
    form_class = Teamwiseform
    template_name = 'superadmin/teamwise_form.html'
    success_url = 'QMS:teamwiseview'

    def get_success_url(self):
        return reverse_lazy(self.success_url)

    def post(self, request, *args, **kwargs):
        form = Teamwiseform(request.POST)
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        form.save()
        return HttpResponseRedirect(self.get_success_url())


class TeamwiseUpdate(UpdateView):
    model = Teamwise
    form_class = Teamwiseform
    template_name = 'superadmin/teamwise_form.html'
    success_url = 'QMS:teamwiseview'

    def get_success_url(self):
        return reverse_lazy(self.success_url)

    def form_valid(self, form):
        form = self.get_form()
        form.save()
        return HttpResponseRedirect(self.get_success_url())

class TeamwiseDelete(DeleteView):
     def ObjectDelete(request,pk):
         object=Teamwise.objects.get(id=pk)
         object.delete()
         return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
