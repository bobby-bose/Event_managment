# Generated by Django 3.2 on 2021-04-26 07:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0003_event_guest_number'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='rsvp_url',
            field=models.CharField(blank=True, max_length=400, null=True),
        ),
    ]
