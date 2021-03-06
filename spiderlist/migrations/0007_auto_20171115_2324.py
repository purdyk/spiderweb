# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2017-11-15 23:24
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('spiderlist', '0006_auto_20171115_2256'),
    ]

    operations = [
        migrations.AlterField(
            model_name='report',
            name='url',
            field=models.CharField(db_index=True, default='https://nzb.cat/', max_length=400),
        ),
        migrations.AlterIndexTogether(
            name='report',
            index_together=set([('guid', 'url')]),
        ),
    ]
