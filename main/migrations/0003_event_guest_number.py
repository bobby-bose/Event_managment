# Generated by Django 3.2 on 2021-04-25 17:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_alter_event_slug'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='guest_number',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
