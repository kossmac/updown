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

"""
Since dispatch is the first method of this view,
every database query from here and in "sub-methods" get executed atomic.
That will prevent multiple update queries in different requests (select_for_update)
"""


@method_decorator(transaction.atomic, 'dispatch')
class UpdownView(UpdateView):
    # We want to operate on a specific model
    model = UpdownFile
    # We want to use a specific custom form
    form_class = DownloadForm
    # render the context to that template
    template_name = 'updown/updownfile_form.html'

    def get_queryset(self, **kwargs):
        # will return queryset that will lock rows until the transaction ends
        return super(UpdownView, self).get_queryset().select_for_update(**kwargs)

    def get(self, request, *args, **kwargs):
        # do the same stuff as in post request
        return self.post(request, *args, **kwargs)

    def form_valid(self, form):
        # when form is valid, save the object and return a file response of it
        obj = form.save()

        return self.file_response(obj)

    def form_invalid(self, form):
        # when form is invalid and the request method was get, do not display any errors
        if self.request.method == 'GET':
            form.errors.pop('password', None)

        # when the form is invalid, method was post and there are any non_field_errors (expired),
        # set the status code to 410 Gone
        if form.non_field_errors():
            status = 410
            return self.render_to_response(self.get_context_data(form=form, status=status), status=status)

        return super(UpdownView, self).form_invalid(form)

    @staticmethod
    def file_response(obj: UpdownFile):
        # takes an UpdownFile object and returns a http file response of it
        response = FileResponse(obj.file)
        response['Content-Disposition'] = 'attachment; filename="%s"' % obj

        return response


class UpdownFileListView(LoginRequiredMixin, CreateView):
    model = UpdownFile
    # where to go, when successfully created an object
    success_url = reverse_lazy('list')
    template_name = 'updown/updownfile_list.html'

    def get_initial(self):
        # fill the form field owner, with the current user id
        initial = super(UpdownFileListView, self).get_initial()
        initial.update({'owner': self.request.user.pk})

        return initial

    def get_form_class(self):
        # use specific form depending on user
        user = self.request.user

        if user.is_superuser:
            return AdminUploadForm

        return UploadForm

    def get_fileset(self):
        # use filtered by owner queryset
        return super(UpdownFileListView, self).get_queryset().filter(owner=self.request.user)

    def form_valid(self, form):
        # we want to save who uploaded the file, so we save the form, but do not commit it
        file = form.save(commit=False)
        # get the user from the request
        user = self.request.user
        # superusers are able to upload files for different users
        if not user.is_superuser:
            file.owner = user

        # commit the changes
        file.save()

        return super(UpdownFileListView, self).form_valid(form)

    def get_context_data(self, **kwargs):
        # return te context, with our custom fileset appended
        return super(UpdownFileListView, self).get_context_data(
            updownfile_list=self.get_fileset(),
            **kwargs
        )


class UpdownFileListViewImpersonate(UpdownFileListView):

    def get_fileset(self):
        user = self.request.user
        if user.is_superuser:
            try:
                # does a user with requested id exists?
                owner = User.objects.get(pk=self.kwargs.get('owner_id'))
                # return filtered queryset with requested user
                return super(UpdownFileListViewImpersonate, self).get_queryset().filter(owner=owner)
            except ObjectDoesNotExist:
                raise Http404
        else:
            raise Http404


class UpdownDeleteView(LoginRequiredMixin, DeleteView):
    model = UpdownFile
    success_url = reverse_lazy('list')

    def get(self, request, *args, **kwargs):
        # delete without confirmation
        return self.post(request, *args, **kwargs)
