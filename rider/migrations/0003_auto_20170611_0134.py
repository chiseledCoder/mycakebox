# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2017-06-10 20:04
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rider', '0002_auto_20170607_2217'),
    ]

    operations = [
        migrations.AddField(
            model_name='rider',
            name='flag',
            field=models.CharField(choices=[('GREEN', 'GREEN'), ('GREEN', 'GREEN'), ('RED', 'RED')], default='RED', max_length=100),
        ),
        migrations.AddField(
            model_name='rider',
            name='slug',
            field=models.SlugField(default='', unique=True),
        ),
    ]
