# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2015-12-29 06:23
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('spiderlist', '0002_auto_20151229_0506'),
    ]

    operations = [
        migrations.AddField(
            model_name='searchresult',
            name='invalid',
            field=models.BooleanField(default=False),
        ),
    ]
