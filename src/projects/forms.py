from django import forms

from waliki.settings import get_slug

from projects.models import Project

class NewProjectForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super(NewProjectForm, self).__init__(*args, **kwargs)

    class Meta:
        model = Project
        fields = ['title', 'markup']

    # def clean_title(self):
    #     title = self.cleaned_data['title']
    #     if not title:
    #         raise forms.ValidationError(_("The title can't be empty"))
    #     if get_slug(title) != title:
    #         raise forms.ValidationError(_("The title isn't valid"))
    #     if not check_perms(['add_page'], self.user, title):
    #         raise forms.ValidationError(_("You have no permission to create a project with this slug"))
    #     if Page.objects.filter(slug=slug).exists():
    #         raise forms.ValidationError(_("There is already a page with this slug"))
    #    return title


class ReviewerForm(forms.Form):
    user_name = forms.CharField(label='User name', max_length=100)
    can_edit = forms.BooleanField(required=False)