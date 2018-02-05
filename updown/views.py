import os

from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import check_password
from django.core.exceptions import PermissionDenied
from django.http import HttpResponse, Http404
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.http import require_http_methods
from django.views.defaults import bad_request
from django.views.generic import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import FormMixin, DeleteView, CreateView

from myapp.forms import DownloadForm, UploadForm
from myapp.models import UpdownFile


class UpdownFileDetailView(DetailView, FormMixin):

    model = UpdownFile
    form_class = DownloadForm

    def get_context_data(self, **kwargs):
        context_data = super(UpdownFileDetailView, self).get_context_data(**kwargs)

        context_data['form'].initial = {'slug': self.object.slug}
        return context_data


class UpdownFileListView(ListView):

    model = UpdownFile

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(UpdownFileListView, self).dispatch(request, *args, **kwargs)
    
    def get_queryset(self):
        if self.request.user.is_authenticated:
            return super(UpdownFileListView, self).get_queryset().filter(owner=self.request.user)
        else:
            return None

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(UpdownFileListView, self).get_context_data(**kwargs)

        context['upload_form'] = UploadForm

        return context


class UpdownCreateView(CreateView):

    model = UpdownFile
    success_url = reverse_lazy('file-list')
    form_class = UploadForm


class UpdownDeleteView(DeleteView):

    model = UpdownFile
    success_url = reverse_lazy('file-list')


@require_http_methods(['POST', 'GET'])
def download(request, slug=None):
    pass_protection = False
    obj = UpdownFile.objects.get(slug=slug)

    if request.method == 'POST':
        form = DownloadForm(request.POST)
        form.full_clean()
        pass_protection = check_password(form.cleaned_data['password'], obj.password)

    if pass_protection or not obj.is_password_protected:
        if not obj.is_expired:
            if os.path.exists(obj.file.name):
                if obj.max_downloads is not '':
                    obj.max_downloads -= 1
                    obj.save()
                with open(obj.file.name, 'rb') as fh:
                    response = HttpResponse(fh.read())
                    response['Content-Disposition'] = 'attachment; filename=' + os.path.basename(obj.file.name)
                    return response
            raise Http404
        else:
            raise PermissionDenied
    else:
        raise PermissionDenied
