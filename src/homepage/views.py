from django.contrib import messages
from django.contrib.auth import get_user_model
from django.core.urlresolvers import reverse
from django.shortcuts import render, redirect
from django.views.decorators.http import require_http_methods

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
    #messages.add_message(request, messages.SUCCESS, 'Hello world. <a href="#" class="alert-link">Click here</a>')
    # messages.add_message(request, messages.INFO, 'Hello world. <a href="#" class="alert-link">Click here</a> <br> Hello world. <a href="#" class="alert-link">Click here</a>')
    #messages.add_message(request, messages.ERROR, 'Hello world. <a href="#" class="alert-link">Click here</a> Hello world. <a href="#" class="alert-link">Click here</a>     ')
    # user = request.user
    #if user.is_anonymous and first time here:
    #    message "data.header_message"
    #if user.is_anonymous:
    #    message "hello anonymous user."
    # if request.user.is_
    try:
        data = HomePage.objects.get(pk=1)
    except:
        data = {'header': 'Ants', 'header_message': "Reinventing classes", "About": "Art, Nature, Technology, Science"}

    if request.user.is_superuser:
        feedbacks = Feedback.objects.filter(status="n")
        messages.add_message(request, messages.INFO, 'New feedbacks: %d. To the <a href="/admin/" class="alert-link">Admin</a>.' % len(feedbacks))
        for feedback in feedbacks:
            messages.add_message(request, messages.SUCCESS, feedback.message)

    form = FeedbackForm(None)
    template = "homepage/home.html"
    context = {
        'header': data.header,
        'header_message': data.header_message,
        'about': data.about,
        # 'lab_title': data.lab_title,
        # 'school_title': data.school_title,
        # 'lab_message': data.lab_message,
        # 'school_message': data.school_message,
        'feedback_invite': data.feedback_invite,
        'address': data.address,
        'form': form
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
        print 'the form is valid'
        new_feedback = form.save(commit=False)
        new_feedback.ip_address = request_ip
        new_feedback.save()
        messages.add_message(request, messages.SUCCESS, 'Thank you for the feedback!')
        return redirect(reverse('home'))
    messages.add_message(request, messages.ERROR, 'Oops, something went wrong. Please <a href="/#contact" class="alert-link">try again</a>.')
    return redirect('/')


def about_page(request):
    data = User.objects.filter(is_staff=True)

    template = "homepage/about.html"
    context = {
        'users': data,
    }
    return render(request, template, context)