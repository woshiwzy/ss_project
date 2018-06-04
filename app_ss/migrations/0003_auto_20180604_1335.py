# -*- coding: utf-8 -*-
# Generated by Django 1.11.13 on 2018-06-04 13:35
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app_ss', '0002_user_alias_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='BMessage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.IntegerField(default=1, verbose_name='\u6d88\u606f\u7c7b\u578b')),
                ('title', models.CharField(default='', max_length=100)),
                ('content', models.CharField(default='', max_length=200)),
                ('title_cn', models.CharField(default='', max_length=100)),
                ('content_cn', models.CharField(default='', max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Host',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('enable', models.BooleanField(default=True, verbose_name='\u662f\u5426\u53ef\u7528')),
                ('type', models.IntegerField(default=1, verbose_name='1\uff1a\u81ea\u5efa\u7acb\u670d\u52a1\u5668\uff0c2.\u5176\u4ed6\u670d\u52a1\u5668')),
                ('alias', models.CharField(max_length=30, verbose_name='\u522b\u540d')),
                ('available_band', models.IntegerField(default=0, verbose_name='\u53ef\u7528\u7684\u5e26\u5bbd')),
                ('total_band', models.IntegerField(default=500, verbose_name='\u603b\u5e26\u5bbd')),
                ('name', models.CharField(default='\u663e\u793a\u540d\u79f0', max_length=30)),
                ('method', models.CharField(max_length=20)),
                ('password', models.CharField(max_length=20)),
                ('ip', models.CharField(default='', max_length=20)),
                ('port', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='VPLOG',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ip', models.CharField(default='', max_length=20, verbose_name='ip')),
                ('port', models.IntegerField()),
                ('brand', models.CharField(default='', max_length=50, verbose_name='\u624b\u673a\u578b\u53f7')),
                ('country', models.CharField(default='', max_length=10, verbose_name='\u56fd\u5bb6\u4ee3\u7801')),
                ('mac', models.CharField(default='', max_length=50, verbose_name='\u7f51\u5361mac\u5730\u5740')),
            ],
        ),
        migrations.AddField(
            model_name='user',
            name='app_version',
            field=models.CharField(default='', max_length=15, verbose_name='app version'),
        ),
        migrations.AddField(
            model_name='user',
            name='brand',
            field=models.CharField(default='', max_length=50, verbose_name='\u624b\u673a\u578b\u53f7'),
        ),
        migrations.AddField(
            model_name='user',
            name='country',
            field=models.CharField(default='', max_length=10, verbose_name='\u56fd\u5bb6\u4ee3\u7801'),
        ),
        migrations.AddField(
            model_name='user',
            name='disableMessage',
            field=models.CharField(default='', max_length=100, verbose_name='\u65e0\u6cd5\u4f7f\u7528\u7684\u65f6\u5019\u63d0\u793a'),
        ),
        migrations.AddField(
            model_name='user',
            name='enable',
            field=models.BooleanField(default=True, verbose_name='\u662f\u5426\u53ef\u7528'),
        ),
        migrations.AddField(
            model_name='user',
            name='imei',
            field=models.CharField(default='', max_length=50, verbose_name='imei'),
        ),
        migrations.AddField(
            model_name='user',
            name='installationId',
            field=models.CharField(default='', max_length=50, verbose_name='vpninstallId'),
        ),
        migrations.AddField(
            model_name='user',
            name='ip',
            field=models.CharField(default='', max_length=20, verbose_name='ip'),
        ),
        migrations.AddField(
            model_name='user',
            name='mac',
            field=models.CharField(default='', max_length=50, verbose_name='\u7f51\u5361mac\u5730\u5740'),
        ),
        migrations.AddField(
            model_name='user',
            name='remaining_bytes',
            field=models.IntegerField(default=0, verbose_name='\u5269\u4f59\u6d41\u91cf'),
        ),
        migrations.AddField(
            model_name='user',
            name='system_version',
            field=models.CharField(default='', max_length=20, verbose_name='\u64cd\u4f5c\u7cfb\u7edf\u7248\u672c'),
        ),
        migrations.AddField(
            model_name='user',
            name='usedByte',
            field=models.IntegerField(default=0, verbose_name='\u5df2\u7ecf\u4f7f\u7528\u7684\u6d41\u91cf'),
        ),
        migrations.AddField(
            model_name='vplog',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
