from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Permission
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404, Http404

from authtools.models import User
from waliki.models import ACLRule
from waliki.signals import page_saved

from .models import Project
from .forms import NewProjectForm, ReviewerForm

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

@login_required
def get_name(request, slug):
    p = get_object_or_404(Project, slug=slug)
    if request.user != p.creator:
        raise Http404('Unknown user')
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = ReviewerForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            try:
                u = User.objects.get(name=form.cleaned_data['user_name'])
            except:
                return HttpResponseRedirect("/p/" + slug + "/_allow/")
            if p.creator == request.user:
                p.reviewers.add(u)
                try:
                    newrule = ACLRule(name="%s on %s"%(u.name,p.slug), slug=p.slug, apply_to='explicit')
                    newrule.save()
                except:
                    return HttpResponseRedirect("/p/" + slug + "/_allow/")
                try:
                    newrule.users.add(u)
                    newrule.permissions.add(Permission.objects.get(codename='view_page'))
                    if form.cleaned_data['can_edit']==True:
                        newrule.permissions.add(Permission.objects.get(codename='change_page'))
                    p.save()
                    newrule.save()
                except:
                    return HttpResponseRedirect("/p/" + slug + "/_allow/")
            # redirect to a new URL:
            return HttpResponseRedirect('/')

    # if a GET (or any other method) we'll create a blank form
    else:
        form = ReviewerForm()

    return render(request, 'projects/add_reviewer.html', {'form': form, 'slug':slug})



# from waliki.models import ACLRule
# from authtools.models import User
# from django.contrib.auth.models import Permission


# g = User.objects.get(name="wouter")
# p = Project.objects.get(reviewers=g)
# perm = Permission.objects.get(codename="view_page")

# newrule = ACLRule(name="%s on %s"%(g.name,p.slug), slug=p.slug, apply_to='explicit')

# newrule.users.add(g)
# newrule.permissions.add('view_page')
