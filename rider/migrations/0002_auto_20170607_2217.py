# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2017-06-07 16:47
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('rider', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='rider',
            old_name='rider_address',
            new_name='address',
        ),
        migrations.RenameField(
            model_name='rider',
            old_name='rider_alt_phone_number',
            new_name='alt_phone_number',
        ),
        migrations.RenameField(
            model_name='rider',
            old_name='rider_first_name',
            new_name='first_name',
        ),
        migrations.RenameField(
            model_name='rider',
            old_name='rider_last_name',
            new_name='last_name',
        ),
        migrations.RenameField(
            model_name='rider',
            old_name='rider_locality',
            new_name='locality',
        ),
        migrations.RenameField(
            model_name='rider',
            old_name='rider_phone_number',
            new_name='phone_number',
        ),
    ]