# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-01-05 05:15
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('spiderlist', '0004_auto_20151229_0949'),
    ]

    operations = [
        migrations.AddField(
            model_name='matchedfile',
            name='missing',
            field=models.BooleanField(default=False),
        ),
    ]