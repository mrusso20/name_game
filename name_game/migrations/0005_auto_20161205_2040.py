# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-12-06 01:40
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('name_game', '0004_auto_20161205_2002'),
    ]

    operations = [
        migrations.CreateModel(
            name='BlockID',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('b_id', models.CharField(max_length=1)),
                ('long_name', models.CharField(max_length=8)),
            ],
        ),
        migrations.AlterField(
            model_name='person',
            name='block',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='name_game.BlockID'),
        ),
    ]
