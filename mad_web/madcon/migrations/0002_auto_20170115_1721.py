# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-01-15 23:21
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('madcon', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='madconapplication',
            name='status',
            field=models.CharField(choices=[('P', 'Pending'), ('A', 'Accepted'), ('W', 'Waitlisted'), ('R', 'Rejected'),
                                            ('C', 'Confirmed')], max_length=1),
        ),
    ]
