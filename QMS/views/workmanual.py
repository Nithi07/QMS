from django.http import HttpResponse, HttpResponseRedirect
from django.db import transaction
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, ListView, UpdateView
from QMS.form.workmanualform import WorkManualform
from QMS.form.workmanualform import ManualCheckListFormSet
from QMS.form.workmanualform import ManualCheckListForm
from QMS.models import WorkManual
from QMS.models import ManualCheckList


class WorkManualListview(ListView):
    model = WorkManual
    template_name = 'superadmin/workmanual_view.html'

    def get_context_data(self, **kwargs):
        workmanual = self.model.objects.all().order_by('pk')
        obj = {'workmanual': workmanual}
        return obj


class WorkManualCreate(CreateView):
    model = WorkManual
    template_name = 'superadmin/workmanual_form.html'
    form_class = WorkManualform
    success_url = 'workmanualview'

    def get_context_data(self, **kwargs):
        data = super(WorkManualCreate, self).get_context_data(**kwargs)
        data['formset']=ManualCheckListFormSet()
        if self.request.POST:
            data['activity'] = ManualCheckListFormSet(self.request.POST)
        else:
            data['activity'] = ManualCheckListFormSet()
        return data

    def form_valid(self, form):
        context = self.get_context_data()
        activity = context['activity']
        with transaction.atomic():
            self.object = form.save()
            if activity.is_valid():
                activity.instance = self.object
                activity.save()
        return super(WorkManualCreate, self).form_valid(form)

    def get_success_url(self):
        return reverse_lazy('QMS:workmanualview')


class WorkManualUpdate(UpdateView):
    model = WorkManual
    form_class = WorkManualform
    template_name = 'superadmin/workmanual_form.html'
    success_url = 'QMS:workmanualview'

    def get_context_data(self, **kwargs):
        data = super(WorkManualUpdate, self).get_context_data(**kwargs)
        data['form'] = WorkManualform(instance=self.object)
        data['formset']=ManualCheckListFormSet(instance=self.object)
        if self.request.POST:
            data['activity'] = ManualCheckListFormSet(self.request.POST, instance=self.object)
        else:
            data['activity'] = ManualCheckListFormSet(instance=self.object)
        return data

    def form_valid(self, form):
        context = self.get_context_data()
        activity = context['activity']
        with transaction.atomic():
            self.object = form.save()
            if activity.is_valid():
                activity.instance = self.object
                activity.save()
        return super(WorkManualUpdate, self).form_valid(form)

    def get_success_url(self):
        return reverse_lazy('QMS:workmanualview')


class WorkManuaDelete(DeleteView):
    def ObjectDelete(request,pk):
        object=WorkManual.objects.get(id=pk)
        object.delete()
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


class WorkManualaddnewCreate(CreateView):
    model = WorkManual
    template_name = 'superadmin/workmanual_form.html'
    form_class = WorkManualform
    success_url = 'QMS:workmanualview'

    def get_object(self):
        return self.model.objects.get(pk=self.kwargs["pk"])

    def get_context_data(self, **kwargs):
        data = super(WorkManualaddnewCreate, self).get_context_data(**kwargs)
        self.object=self.get_object()
        if self.request.POST:
            data['activity'] = ManualCheckListFormSet(self.request.POST, instance=self.object)
        else:
            data['activity'] = ManualCheckListFormSet(instance=self.object)
        return data

    def form_valid(self, form):
        context = self.get_context_data()
        activity = context['activity']
        with transaction.atomic():
            self.object = form.save()
            if activity.is_valid():
                activity.instance = self.object
                activity.save()
        return super(WorkManualaddnewCreate, self).form_valid(form)

    def get_success_url(self):
        return reverse_lazy('QMS:workmanualview')
