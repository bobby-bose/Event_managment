from django.urls import path
from main.views import *

urlpatterns = [
    path('', index, name='index'),
    path('dashboard/', dashboard, name='dashboard'),
    path('dashboard/<slug:slug>', dashboard, name='dashboard'),
    path('rsvp_url/',rsvp_url, name='rsvp_url'),
    path('create_event/', create_event, name='create_event'),
    path('delete_event/<slug:slug>', delete_event, name='delete_event'),
    path('rsvp/<slug:slug>',rsvp,name='rsvp'),
    path('event_dashboard/<slug:slug>', event_dashboard, name='event_dashboard'),

]
