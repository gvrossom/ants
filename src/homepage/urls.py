from django.conf.urls import url
from django.utils.translation import ugettext_lazy as _

from . import views


urlpatterns = [
    url(r'^$', views.home_page, name='home'),
    url(_(r'^feedback/$'), views.feedback, name="feedback"),
    url(r'^about/$', views.about_page, name='about'),
]