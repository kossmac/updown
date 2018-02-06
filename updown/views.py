from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.http import FileResponse
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic.detail import DetailView
from django.views.generic.edit import FormMixin, DeleteView, UpdateView, CreateView

from myapp.forms import DownloadForm, UploadForm, AdminUploadForm
from myapp.models import UpdownFile


class UpdownFileDetailView(DetailView, FormMixin):

    model = UpdownFile
    form_class = DownloadForm

    def get_context_data(self, **kwargs):
        context_data = super(UpdownFileDetailView, self).get_context_data(**kwargs)

        context_data['form'].initial = {'slug': self.object.slug}
        return context_data


class UpdownFileListView(LoginRequiredMixin, CreateView):

    model = UpdownFile
    success_url = reverse_lazy('manage')
    template_name = 'myapp/updownfile_list.html'

    def get_initial(self):
        initial = super(UpdownFileListView, self).get_initial()
        initial.update({'owner': self.request.user.pk})

        return initial

    def get_form_class(self):
        user = self.request.user

        if user.is_superuser:
            return AdminUploadForm

        return UploadForm

    def dispatch(self, request, *args, **kwargs):
        return super(UpdownFileListView, self).dispatch(request, *args, **kwargs)
    
    def get_fileset(self):
        if self.request.user.is_authenticated:
            return super(UpdownFileListView, self).get_queryset().filter(owner=self.request.user)
        else:
            return None

    def form_valid(self, form):
        file = form.save(commit=False)
        user = self.request.user
        if not user.is_superuser:
            file.owner = user

        file.save()

        return super(UpdownFileListView, self).form_valid(form)

    def get_context_data(self, **kwargs):
        return super(UpdownFileListView, self).get_context_data(updownfile_list=self.get_fileset(), **kwargs)


class UpdownDeleteView(DeleteView):

    model = UpdownFile
    success_url = reverse_lazy('manage')


class UpdownUpdateView(UpdateView):

    model = UpdownFile
    form_class = DownloadForm

    def form_valid(self, form):
        response = FileResponse(self.object.file)
        response['Content-Disposition'] = 'attachment; filename="%s"' % self.object.file
        form.save()

        return response

    def form_invalid(self, form):
        return render(self.request, 'myapp/updownfile_detail.html', context={
            'form_errors': form.errors,
            'updownfile': self.object,
        }, status=410)


class UserLoginView(LoginView):
    template_name = 'admin/login.html'
