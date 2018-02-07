from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.db import transaction
from django.http import FileResponse, Http404
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic.edit import DeleteView, UpdateView, CreateView

from .forms import DownloadForm, UploadForm, AdminUploadForm
from .models import UpdownFile


@method_decorator(transaction.atomic, 'dispatch')
class UpdownView(LoginRequiredMixin, UpdateView):
    model = UpdownFile
    form_class = DownloadForm
    template_name = 'updown/updownfile_form.html'

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
    success_url = reverse_lazy('list')
    template_name = 'updown/updownfile_list.html'

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
        return super(UpdownFileListView, self).get_context_data(
            updownfile_list=self.get_fileset(),
            pipi='toll',
            **kwargs
        )


class UpdownFileListViewImpersonate(UpdownFileListView):

    def get_fileset(self):
        user = self.request.user
        try:
            owner = User.objects.get(pk=self.kwargs.get('owner_id'))
        except ObjectDoesNotExist:
            raise Http404

        if user.is_authenticated and user.is_superuser:
            return super(UpdownFileListViewImpersonate, self).get_queryset().filter(owner=owner)
        else:
            return None


class UpdownDeleteView(LoginRequiredMixin, DeleteView):

    model = UpdownFile
    success_url = reverse_lazy('list')

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)
