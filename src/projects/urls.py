from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^new/$', views.new_project, name='new_project'),
]