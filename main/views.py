from django.utils import timezone

import datetime
import urllib.parse

from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from django.shortcuts import render, redirect

from main.models import Event, RSVP, Message, Gift


def index(request):
    return render(request, 'main/index.html')


@login_required
def dashboard(request,slug=None):
    host = request.user
    quote_string = ""
    if slug is None:
        the_event = Event.objects.filter(host=host).last()
        if not the_event:
            context = {}
            return render(request, 'main/dashboard.html', context)

        quote_string = urllib.parse.quote(the_event.rsvp_url)
    else:
        the_event = Event.objects.get(slug=slug,host=host)
    events = Event.objects.filter(host=host).order_by('-id')
    rsvp_responses = RSVP.objects.filter(event=the_event)
    # computing summery
    total_response = rsvp_responses.count()
    total_guests = rsvp_responses.filter(response='yes').aggregate(Sum('guest_number'))['guest_number__sum']
    total_yes = rsvp_responses.filter(response='yes').count()
    total_no = rsvp_responses.filter(response='no').count()

    summary = {'total_response':total_response,'total_guests':total_guests,
               'total_yes':total_yes,'total_no':total_no,"quote_string":quote_string}
    #computing summery end

    #checking if event has already ended
    now = timezone.now()
    if not the_event.ended:
        if the_event.end_date < now :
            the_event.ended = True
            the_event.save()
    #checking if event has already ended end


    context = {'events':events, 'the_event':the_event,'quote_string':quote_string,'rsvp_responses':rsvp_responses,'summary':summary}
    return render(request, 'main/dashboard.html', context)



@login_required
def create_event(request):
    if request.POST:
        host = request.user
        name = request.POST.get('name')
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')
        location = request.POST.get('location')
        guest_number = request.POST.get('guest_number')
        if not guest_number:
            guest_number = None
        description = request.POST.get('description')
        obj = Event(host=host,name=name, start_date=start_date,end_date=end_date,location=location,guest_number=guest_number,description=description)
        obj.save()
        messages.success(request, 'Event created successfully')
        slug = obj.slug
        request.session['slug'] = slug
        return redirect('rsvp_url')
    context = {}
    return render(request, 'main/create_event2.html', context)

@login_required
def delete_event(request,slug):
    host = request.user
    event = Event.objects.get(slug=slug, host=host)
    event.delete()
    messages.success(request, f'{event.name} has been deleted')
    return redirect('dashboard')


@login_required
def rsvp_url(request):
    slug = request.session['slug']
    domain = settings.ALLOWED_HOSTS[0]
    print(domain)
    rsvp_event_url = f'https://{domain}/rsvp/{slug}'
    # saving rsvp url to event modal
    event = Event.objects.get(slug=slug)
    event.rsvp_url = rsvp_event_url
    event.save()
    #saved
    quote_string = urllib.parse.quote(rsvp_event_url)
    context = {'rsvp_event_url':rsvp_event_url,'quote_string':quote_string}
    return render(request, 'main/rsvp_url.html', context)

def rsvp(request,slug):
    the_event = Event.objects.get(slug=slug)
    if request.POST:
        name = request.POST.get('name')
        email = request.POST.get('email')
        response = request.POST.get('attendence')
        guest_number = request.POST.get('guest_number')
        obj = RSVP(event=the_event,name=name,email=email,response=response,guest_number=guest_number)
        obj.save()
        messages.success(request, 'Thanks for your response')
        return redirect('event_dashboard',slug)
    context = {'the_event':the_event}
    return render(request, 'main/rsvp.html', context)

def event_dashboard(request,slug):
    the_event = Event.objects.get(slug=slug)
    messages = Message.objects.filter(event=the_event)
    gifts = Gift.objects.filter(event = the_event)
    context = {'messages':messages,'gifts':gifts}
    return render(request, 'main/event_dashboard.html', context)

