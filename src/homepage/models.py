from __future__ import unicode_literals

from django.db import models
from django.utils.translation import ugettext_lazy as _


class HomePage(models.Model):
    header = models.CharField(max_length=120, default="The Project")
    header_message = models.CharField(max_length=200, default="The Project")
    about = models.CharField(max_length=200, null=True, blank=True)
    lab_title = models.CharField(max_length=120, null=True, blank=True)
    lab_message = models.CharField(max_length=455, null=True, blank=True)
    school_title = models.CharField(max_length=120, null=True, blank=True)
    school_message = models.CharField(max_length=200, null=True, blank=True)
    feedback_invite = models.CharField(max_length=120, null=True, blank=True)
    address = models.CharField(max_length=120, null=True, blank=True)
    #services =
    #portfolio = 
    #form = models.BooleanField
    #contact = 

    def __unicode__(self):
        return self.header


FEEDBACK_STATUS_CHOICES = (
    ('n', 'New'),
    ('r', 'Read'),
    ('a', 'Answered'),
)

class Feedback(models.Model):

    name =  models.CharField(max_length=30)
    email = models.EmailField()
    # phone = models.PositiveIntegerField(blank=True, null=True)
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    ip_address = models.GenericIPAddressField(protocol='both', null=True, blank=True)
    status = models.CharField(max_length=1, choices=FEEDBACK_STATUS_CHOICES, default="n")

    class Meta:
        verbose_name = _('Feedback')
        verbose_name_plural = _('Feedbacks')

    def __str__(self):
        return self.email




# class Message(models.Model):
#     content = models.CharField(max_length=120, default="Because CookThis website uses cookies, because")
#     timestamp = models.DateTimeField(auto_now_add = True, auto_now=False)

#     def __unicode__(self):
#         return self.header

#     def get_date(self):
#         obj_date = str(self.timestamp)[:10]
#         return obj_date