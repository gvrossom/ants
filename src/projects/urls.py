from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^new/$', views.new_project, name='new_project'),
    url(r'^(?P<slug>[a-zA-Z0-9-_\/]+)/_allow/$', views.get_name, name="add_reviewer"),
    url(r'^(?P<slug>[a-zA-Z0-9-_\/]+)/_mkpublic/$', views.make_public, name="make_public"),
]