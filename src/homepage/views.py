from django.contrib import messages
from django.contrib.auth import get_user_model
from django.core.urlresolvers import reverse
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q
from django.shortcuts import render, redirect, render_to_response, get_object_or_404, get_list_or_404, Http404
from django.template import RequestContext
from django.views.decorators.http import require_http_methods


import re
from markdown import Markdown

from waliki.models import Page

from projects.models import Project

User = get_user_model()

from .models import HomePage, Feedback
from .forms import FeedbackForm

def get_ip(request):
    try:
        x_forward = request.META.get("HTTP_X_FORWARDED_FOR")
        if x_forward:
            ip = x_forward.split(",")[0]
        else:
            ip = request.META.get("REMOTE_ADDR")
    except:
        ip = ""

    return ip


def home_page(request):

    pattern = "^[a-z]+$"
    # private_patern = r"([a-fA-F\d]{32})"
    pages = Project.objects.all()
    # public = [page for page in pages if re.match(pattern, page.slug)]
    public = [page for page in pages if page.is_public()]

    # users = User.objects.all()
    if request.user.is_authenticated():
        #Project.objects.filter(Q(creator=g)|Q(reviewers=g))

        projects = Project.objects.filter( Q(creator=request.user) | Q(reviewers=request.user) ).order_by('-last_updated').distinct()
        
    else:
        projects = None

    # if request.user.is_superuser:
    #     feedbacks = Feedback.objects.filter(status="n")
    #     if feedbacks:
    #         messages.add_message(request, messages.INFO, 'New feedbacks: %d. To the <a href="/admin/" class="alert-link">Admin</a>.' % len(feedbacks))
    #         for feedback in feedbacks:
    #             messages.add_message(request, messages.SUCCESS, feedback.message)

    # form = FeedbackForm(None)
    template = "homepage/home.html"
    context = {
        # 'about': data['about'],
        'pages': public,
        'projects': projects,
        # 'lab_title': data.lab_title,
        # 'school_title': data.school_title,
        # 'lab_message': data.lab_message,
        # 'school_message': data.school_message,
        #'feedback_invite': data['feedback_invite'],
        #'address': data['address'],
        #'form': form
    }
    return render(request, template, context)


@require_http_methods(['POST'])
def feedback(request):
    form = FeedbackForm(request.POST)
    request_ip = get_ip(request)
    feedbacks = Feedback.objects.filter(ip_address=request_ip)
    if len(feedbacks) > 5: 
        messages.add_message(request, messages.WARNING, "Seems like you like us a lot, unfortunately we have to limit you to make sure we can handle all requests.")
        return redirect('/')
    if form.is_valid():
        new_feedback = form.save(commit=False)
        new_feedback.ip_address = request_ip
        new_feedback.save()
        messages.add_message(request, messages.SUCCESS, 'Thank you for the feedback!')
        return redirect(reverse('home'))
    messages.add_message(request, messages.ERROR, 'Oops, something went wrong. Please <a href="/#contact" class="alert-link">try again</a>.')
    return redirect('/')





def is_number(s):
    try:
        int(s)
        return True
    except ValueError:
        return False


def detail_page(request, slug):
    # slug_split = slug.split("/")
    # level = len(slug_split)
    # part_of_many = False
    # for word in slug_split:
    #     if is_number(word):
    #         part_of_many = True
    #         current_position = int(word)
    # pattern = "^[a-z]+$"

    # if not re.match(pattern, slug):
    p = get_object_or_404(Project, slug=slug)
    if not p.is_public():
        if request.user != p.creator and request.user not in p.reviewers.all():
            raise Http404('User unknown.') 
    if p.markup == "Markdown":
        md = Markdown(extensions=['markdown.extensions.toc'])
        html = md.convert(p.raw)
        toc = md.toc
    else:
        toc = None


    # sub_data = Page.objects.filter( slug__contains= slug).order_by("title")
    # one_level_up = []
    # for x in sub_data:
    #     if len(x.slug.split("/")) == level + 1:
    #         one_level_up.append(x)

    # if level == 1:
    #     data = Page.objects.all()
    #     pattern = "^[a-z]+$"
    #     same_level_data = [p for p in data if re.match(pattern, p.slug)]
    #     parent = None
    #     prev_slug = None
    #     next_slug = None
    # else:
    #     parent_slug = "/".join(slug_split[:level-1])
    #     data = Page.objects.filter( slug__contains=parent_slug).order_by("title")
    #     same_level_data = []
    #     for x in data:
    #         if len(x.slug.split("/")) == level:
    #             same_level_data.append(x)
    #         if x.slug == parent_slug:
    #             parent = x

    #     if part_of_many:
    #         prev_slug = parent_slug + "/" + str(current_position-1)
    #         next_slug = parent_slug + "/" + str(current_position+1)
    #         if current_position == 1:
    #             prev_slug = None
    #         if current_position == len(same_level_data):
    #             next_slug = None
    #     else:
    #         prev_slug = None
    #         next_slug = None 

    template = "homepage/detail.html"

    context = {
        'slug': slug,
        'page': p,
        'toc': toc,
        # 'data': same_level_data,
        # 'sub_data': one_level_up,
        # 'parent': parent,
        # 'previous': prev_slug,
        # 'next': next_slug,
    }
    return render(request, template, context)


# def my_custom_page_not_found_view(request):
#     return render(request, template="404.html")




# def handler404(request):
#     response = render_to_response('404.html', {},
#                                   context_instance=RequestContext(request))
#     response.status_code = 404
#     return response


# def handler500(request):
#     response = render_to_response('500.html', {},
#                                   context_instance=RequestContext(request))
#     response.status_code = 500
#     return response