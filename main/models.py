from django.contrib.auth.models import User
from django.db import models
from main.utils import unique_slug_generator
# Create your models here.
from django.db.models.signals import pre_save


class Event(models.Model):
    host = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=500, blank=False)
    slug = models.SlugField(max_length=500, blank=True)
    start_date = models.DateTimeField(blank=False)
    end_date = models.DateTimeField(blank=False)
    location = models.CharField(max_length=400, blank=False)
    guest_number = models.IntegerField(blank=True, null=True)
    description = models.TextField(blank=True)
    rsvp_url = models.CharField(max_length=400, blank=True, null=True)
    date_created = models.DateTimeField(auto_now_add=True)
    ended = models.BooleanField(default=False)

    def __str__(self):
        return str(self.name) + ' by ' + str(self.host)

class Gift(models.Model):
    event = models.ForeignKey(Event,on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True, null=True)
    link = models.CharField(max_length=2055,null=True)
    locked = models.BooleanField(default=False,null=True)


class Message(models.Model):
    event =models.ForeignKey(Event, on_delete=models.CASCADE)
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    message = models.TextField()
    date_created = models.DateTimeField(auto_now_add=True)


class RSVP(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=524)
    response = models.CharField(max_length=300, default='yes')
    guest_number = models.IntegerField()
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.name)


def slug_generator(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)


pre_save.connect(receiver=slug_generator, sender=Event)




