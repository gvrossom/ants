from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect

from waliki.signals import page_saved

from .models import Project
from .forms import NewProjectForm

# def new_project(request, title):
#     slug = slug.strip('/')
#     just_created = False
#     try:
#         page = Page.objects.get(title=title)
#     except Page.DoesNotExist:
#         if request.method == 'POST':
#             page = Page(title=title, creator=request.user)
#             page.raw = ""
#             page_saved.send(sender=edit,
#                             page=page,
#                             author=request.user,
#                             message=_("Page created"),
#                             form_extra_data={})
#             just_created = True
#         else:
# return redirect('waliki_detail', slug)

@login_required
def new_project(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = NewProjectForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            project = Project(title=form.cleaned_data['title'], creator=request.user, markup=form.cleaned_data['markup'])
            project.save()
            page_saved.send(sender=new_project,
                            page=project,
                            author=request.user,
                            message="Page created",
                            form_extra_data={})
            # redirect to a new URL:
            return HttpResponseRedirect(project.get_absolute_url())

    # if a GET (or any other method) we'll create a blank form
    else:
        form = NewProjectForm()

    return render(request, 'projects/new.html', {'form': form})


