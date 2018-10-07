# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-05-26 17:36
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('students', '0007_auto_20180504_1816'),
    ]

    operations = [
        migrations.AddField(
            model_name='group',
            name='slug',
            field=models.SlugField(default='', max_length=256),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='student',
            name='slug',
            field=models.SlugField(default='', max_length=256),
            preserve_default=False,
        ),
    ]