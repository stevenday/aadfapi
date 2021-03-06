# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-06-25 21:21
from __future__ import unicode_literals

import django.contrib.gis.db.models.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0003_auto_20170624_2241'),
    ]

    operations = [
        migrations.CreateModel(
            name='Ward',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('objectid', models.IntegerField()),
                ('wd16cd', models.CharField(max_length=80)),
                ('wd16nm', models.CharField(max_length=80)),
                ('wd16nmw', models.CharField(max_length=80)),
                ('lad16cd', models.CharField(max_length=80)),
                ('lad16nm', models.CharField(max_length=80)),
                ('bng_e', models.IntegerField()),
                ('bng_n', models.IntegerField()),
                ('long', models.FloatField()),
                ('lat', models.FloatField()),
                ('st_areasha', models.FloatField()),
                ('st_lengths', models.FloatField()),
                ('geom', django.contrib.gis.db.models.fields.MultiPolygonField(srid=4326)),
            ],
        ),
    ]
