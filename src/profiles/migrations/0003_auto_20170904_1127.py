# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-09-04 11:27
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0002_auto_20170904_1104'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='UserData',
            new_name='Profile',
        ),
    ]
