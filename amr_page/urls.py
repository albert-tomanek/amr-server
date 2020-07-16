from django.urls import path, re_path

from . import views

urlpatterns = [
    path   ('', views.index, name='index'),
    re_path('^amr-data/[0123456789abcdef]+.amr$', views.get_amrdata),
]
