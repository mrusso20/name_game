# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-12-06 05:21
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('name_game', '0006_scorekeeper'),
    ]

    operations = [
        migrations.AlterField(
            model_name='scorekeeper',
            name='active_score',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='scorekeeper',
            name='high_score',
            field=models.IntegerField(default=0),
        ),
    ]
