# -*- coding: utf-8 -*-
# Generated by Django 1.9.8 on 2016-07-31 22:56
from __future__ import unicode_literals

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('go', '0003_auto_20160731_1747'),
    ]

    operations = [
        migrations.AlterField(
            model_name='go',
            name='id',
            field=models.CharField(error_messages={'unique': 'A Go Link with that ID already exists.'},
                                   help_text='Required. 255 characters or fewer. Letters, digits and @/./+/-/_ only.',
                                   max_length=255, primary_key=True, serialize=False, unique=True, validators=[
                    django.core.validators.RegexValidator('^[a-zA-Z0-9_-]+$',
                                                          'Enter a valid Go ID. This value may contain only letters, numbers and @/./+/-/_ characters.')],
                                   verbose_name='ID for Go'),
        ),
        migrations.AlterField(
            model_name='go',
            name='url',
            field=models.CharField(help_text='Required. 255 characters or fewer.', max_length=255, validators=[
                django.core.validators.RegexValidator(
                    '(?i)\\b((?:[a-z][\\w-]+:(?:/{1,3}|[a-z0-9%])|www\\d{0,3}[.]|[a-z0-9.\\-]+[.][a-z]{2,4}/)(?:[^\\s()<>]+|\\(([^\\s()<>]+|(\\([^\\s()<>]+\\)))*\\))+(?:\\(([^\\s()<>]+|(\\([^\\s()<>]+\\)))*\\)|[^\\s`!()\\[\\]{};:\\\'".,<>?«»“”‘’]))',
                    'Enter a valid Go URL.')], verbose_name='URL'),
        ),
    ]
