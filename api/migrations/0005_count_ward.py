# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-06-26 07:05
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0004_ward'),
    ]

    operations = [
        migrations.AddField(
            model_name='count',
            name='ward',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='api.Ward'),
        ),
    ]
