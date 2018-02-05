"""updown URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path

from updown.views import UpdownFileDetailView, download, UpdownFileListView, UpdownDeleteView, UpdownCreateView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('request/<slug:slug>', UpdownFileDetailView.as_view(), name='request'),
    path('download/<slug:slug>', download, name='download'),
    path('add/', UpdownCreateView.as_view(), name='add'),
    path('delete/<slug:slug>', UpdownDeleteView.as_view(), name='delete'),
    path('manage/', UpdownFileListView.as_view(), name='file-list'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
