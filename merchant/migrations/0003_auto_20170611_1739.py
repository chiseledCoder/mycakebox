# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2017-06-11 12:09
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('merchant', '0002_auto_20170606_2122'),
    ]

    operations = [
        migrations.RenameField(
            model_name='merchantaccount',
            old_name='origin_address',
            new_name='address',
        ),
    ]
