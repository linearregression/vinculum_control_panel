# -*- coding: utf-8 -*-
# Generated by Django 1.9.8 on 2016-08-03 23:46
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('vinculum', '0002_auto_20160803_2322'),
    ]

    operations = [
        migrations.AlterField(
            model_name='inputpath',
            name='remote_resource',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='input_paths', to='vinculum.RemoteResources'),
        ),
    ]