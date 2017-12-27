from django.contrib import admin

from .models import Project


class ProjectAdmin(admin.ModelAdmin):
    list_display = [
        'page_ptr',
        'creator',
    ]

    class Meta:
        model = Project

admin.site.register(Project, ProjectAdmin)