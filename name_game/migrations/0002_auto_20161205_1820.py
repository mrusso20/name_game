# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-12-05 23:20
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('name_game', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Block',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('block_id', models.CharField(max_length=1)),
            ],
        ),
        migrations.RemoveField(
            model_name='person',
            name='name',
        ),
        migrations.RemoveField(
            model_name='person',
            name='picture',
        ),
        migrations.AddField(
            model_name='person',
            name='f_name',
            field=models.CharField(default='', max_length=15),
        ),
        migrations.AddField(
            model_name='person',
            name='l_name',
            field=models.CharField(default='', max_length=15),
        ),
        migrations.AddField(
            model_name='person',
            name='p_id',
            field=models.CharField(default='', max_length=10),
        ),
        migrations.AddField(
            model_name='block',
            name='p_block',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='name_game.Person'),
        ),
    ]
