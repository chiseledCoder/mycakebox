# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2017-04-22 15:52
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Rider',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rider_id', models.CharField(default='ABC', max_length=10, unique=True)),
                ('rider_first_name', models.CharField(max_length=100)),
                ('rider_last_name', models.CharField(max_length=100)),
                ('rider_address', models.CharField(max_length=100)),
                ('rider_locality', models.CharField(max_length=100)),
                ('rider_phone_number', models.CharField(max_length=15)),
                ('rider_alt_phone_number', models.CharField(blank=True, max_length=15, null=True)),
            ],
        ),
    ]
