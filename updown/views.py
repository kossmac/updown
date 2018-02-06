from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.db import transaction
from django.http import FileResponse
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic.edit import DeleteView, UpdateView, CreateView

from myapp.forms import DownloadForm, UploadForm, AdminUploadForm
from myapp.models import UpdownFile


@method_decorator(transaction.atomic, 'dispatch')
class UpdownView(UpdateView):
    model = UpdownFile
    form_class = DownloadForm
    template_name = 'myapp/updownfile_form.html'

    def get_queryset(self, **kwargs):
        return super(UpdownView, self).get_queryset().select_for_update(**kwargs)

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)

    def form_valid(self, form):
        obj = form.save()

        return self.file_response(obj)

    def form_invalid(self, form):
        if self.request.method == 'GET':
            form.errors.pop('password', None)

        if form.non_field_errors():
            status = 410
            return self.render_to_response(self.get_context_data(form=form, status=status), status=status)

        return super(UpdownView, self).form_invalid(form)

    @staticmethod
    def file_response(obj: UpdownFile):
        response = FileResponse(obj.file)
        response['Content-Disposition'] = 'attachment; filename="%s"' % obj.file.name

        return response


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


class UserLoginView(LoginView):
    template_name = 'admin/login.html'
