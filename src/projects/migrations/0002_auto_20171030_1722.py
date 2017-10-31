# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2017-10-30 17:22
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='created',
            field=models.DateTimeField(auto_now_add=True, default=datetime.datetime(2017, 10, 30, 17, 22, 1, 846357, tzinfo=utc)),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='project',
            name='last_updated',
            field=models.DateTimeField(auto_now=True, default=datetime.datetime(2017, 10, 30, 17, 22, 11, 808842, tzinfo=utc)),
            preserve_default=False,
        ),
    ]
