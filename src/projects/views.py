from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Permission
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404, Http404

from authtools.models import User
from waliki.models import ACLRule
from waliki.signals import page_saved

from .models import Project
from .forms import NewProjectForm, ReviewerForm



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

@login_required
def get_name(request, slug):
    """

    Get name to create view aclrule with or without edit/change/write permission

    Only staff users can currently add reviewers.

    TODO:

    [x] make sure author doesn't insert himself.
    [] gently fail

    """
    # get related project
    p = get_object_or_404(Project, slug=slug)

    # if request.user != p.creator:
    if request.user.is_staff:
        
        # if this is a POST request we need to process the form data
        if request.method == 'POST':
            # create a form instance and populate it with data from the request:
            form = ReviewerForm(request.POST)
            # check whether it's valid:
            if form.is_valid():
                # process the data in form.cleaned_data as required
                try:
                    u = User.objects.get(name=form.cleaned_data['user_name'])
                except ObjectDoesNotExist:
                    messages.add_message(request, messages.WARNING, 'User name "%s" does not exist.' % form.cleaned_data['user_name'])
                    return HttpResponseRedirect("/p/" + slug + "/_allow/")
                if u == request.user:
                    messages.add_message(request, messages.WARNING, '... I cannot do that right now. Not yet. Maybe one day.')
                    return HttpResponseRedirect("/p/" + slug + "/_allow/")
                if form.cleaned_data['user_name'] == p.creator.name:
                    messages.add_message(request, messages.WARNING, '... I cannot do that right now. Not yet. Maybe one day.')
                    return HttpResponseRedirect("/p/" + slug + "/_allow/")
                p.reviewers.add(u)

                name = '%s on "%s" with read' % (u.name, p.title)
                if form.cleaned_data['can_edit'] == True:
                    name += " and write"
                try:
                    rule = ACLRule.get(name=name, slug=p.slug, apply_to='explicit')
                except:
                    messages.add_message(request, messages.SUCCESS, 'Rule seems new :)')
                else:
                    messages.add_message(request, messages.WARNING, 'Rule already exists.')
                    return HttpResponseRedirect("/p/" + slug + "/_allow/")
                try:
                    newrule = ACLRule(name=name, slug=p.slug, apply_to='explicit')
                    newrule.save()
                    messages.add_message(request, messages.SUCCESS, 'Rule saved.')
                except:
                    messages.add_message(request, messages.WARNING, 'Error when saving aclrule.')
                    return HttpResponseRedirect("/p/" + slug + "/_allow/")
                
                try:
                    newrule.users.add(u)
                    newrule.permissions.add(Permission.objects.get(codename='view_page'))
                    if form.cleaned_data['can_edit']==True:
                        newrule.permissions.add(Permission.objects.get(codename='change_page'))   
                except:
                    messages.add_message(request, messages.WARNING, 'Error when adding reviewer or permissions to rule.')
                    return HttpResponseRedirect("/p/" + slug + "/_allow/")
                else:
                    p.save()
                    newrule.save()
                    messages.add_message(request, messages.SUCCESS, 'User and permission saved to rule.')
                # redirect to a new URL:
                return HttpResponseRedirect('/')

        # if a GET (or any other method) we'll create a blank form
        else:
            form = ReviewerForm()
    else:
        raise Http404('Nope.')

    return render(request, 'projects/add_reviewer.html', {'form': form, 'slug':slug})


"""
TO DO

[] Project admin view for users with list of reviewers
[] Reviewer delete aclrule view (read and/or write permissions)

"""
