# Generated by Django 3.2 on 2022-07-07 22:13

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userprofile',
            name='default_county',
        ),
        migrations.RemoveField(
            model_name='userprofile',
            name='default_phone_number',
        ),
        migrations.RemoveField(
            model_name='userprofile',
            name='default_street_address2',
        ),
    ]
