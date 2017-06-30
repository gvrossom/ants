from __future__ import unicode_literals

from django.db import models
from django.utils.translation import ugettext_lazy as _

from waliki.models import Page

class Project(Page):
    ref_id = models.CharField(max_length=120, default="", unique=True)

    def __unicode__(self):
        return self.ref_id