# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-09-04 11:04
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='userdata',
            name='activated',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='userdata',
            name='activation_key',
            field=models.CharField(default=11, max_length=120),
            preserve_default=False,
        ),
    ]
