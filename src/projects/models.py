from __future__ import unicode_literals

import hashlib

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

    def save(self, *args, **kwargs):
        self.slug = hashlib.md5(self.title).hexdigest()
        self.slug = self.creator.name + "/" + self.slug
        if not self.path:
            self.path = self.slug + self.markup
        if not self.raw:
            self.raw = "Hello %s,\n\nstart harvesting your seed here.\n\n" % (self.creator.name)
        super(Project, self).save(*args, **kwargs)