from django.contrib import admin

from .models import HomePage, Feedback


class HomePageAdmin(admin.ModelAdmin):
    list_display = [
        'header',
        'header_message',
        'about',
    ]

    class Meta:
        model = HomePage


def make_read(ModelAdmin, request, queryset):
    queryset.update(status='r')
make_read.short_description = "Updates feedback status to: read."


class FeedbackAdmin(admin.ModelAdmin):
    list_display = ['name','email', 'message', 'status', 'timestamp']
    search_fields = ['name', 'email', 'message']
    list_filter = ['status', 'timestamp']
    actions = [make_read]


admin.site.register(HomePage, HomePageAdmin)
admin.site.register(Feedback, FeedbackAdmin)