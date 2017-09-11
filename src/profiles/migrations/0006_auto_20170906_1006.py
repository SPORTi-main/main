# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-09-06 10:06
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('profiles', '0005_badges'),
    ]

    operations = [
        migrations.CreateModel(
            name='Badge',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('badge', models.CharField(max_length=120)),
                ('description', models.TextField(max_length=500)),
                ('image', models.ImageField(default='media/default.png', upload_to='badge_images')),
                ('date_added', models.DateTimeField(auto_now_add=True)),
                ('date_updated', models.DateTimeField(auto_now=True)),
                ('owners', models.ManyToManyField(blank=True, null=True, related_name='badges', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.RemoveField(
            model_name='badges',
            name='owners',
        ),
        migrations.DeleteModel(
            name='Badges',
        ),
    ]