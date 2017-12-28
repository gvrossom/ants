from __future__ import unicode_literals

import hashlib
import datetime

from django.conf import settings
from django.db import models
from django.utils.translation import ugettext_lazy as _

from waliki.models import Page
from waliki.settings import get_slug

class Project(Page):
    page_ptr = models.OneToOneField(
        Page, on_delete=models.CASCADE,
        parent_link=True,
        related_name='project_page'
    )

    creator = models.ForeignKey(
        settings.AUTH_USER_MODEL
        )
    created = models.DateTimeField(auto_now=False, auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)
    reviewers = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name="reviewers")

    # TODO

    # [] check for existing reviewer and permissions
    # [] remove aclrule when removing reviewer
    

    def save(self, *args, **kwargs):
        self.slug = hashlib.md5(self.title).hexdigest()
        self.slug = self.creator.name.lower() + "/" + self.slug
        if not self.path:
            self.path = self.slug + self.markup_.file_extensions[0]
        if not self.raw:
            self.raw = "Author: %s\n\nCreated: %s\n\n" % (self.creator.name, datetime.datetime.now())
        super(Project, self).save(*args, **kwargs)

    def __str__(self):              # __unicode__ on Python 2
        return self.page_ptr.title

    class Meta:
        ordering = ('last_updated',)





