# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-06-26 09:55
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0005_count_ward'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='ward',
            options={'ordering': ['wd16nm']},
        ),
    ]
