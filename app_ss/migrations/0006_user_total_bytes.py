# -*- coding: utf-8 -*-
# Generated by Django 1.11.13 on 2018-06-04 15:07
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_ss', '0005_auto_20180604_1500'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='total_bytes',
            field=models.IntegerField(default=0, verbose_name='\u603b\u6d41\u91cf'),
        ),
    ]
