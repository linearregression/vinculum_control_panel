# -*- coding: utf-8 -*-
# Generated by Django 1.9.8 on 2016-08-04 00:20
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('vinculum', '0005_auto_20160804_0001'),
    ]

    operations = [
        migrations.CreateModel(
            name='InputOutputPath',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('input_path', models.TextField()),
                ('remote_resource', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='io_paths', to='vinculum.RemoteResources')),
            ],
        ),
        migrations.RemoveField(
            model_name='inputpath',
            name='remote_resource',
        ),
        migrations.DeleteModel(
            name='InputPath',
        ),
    ]
