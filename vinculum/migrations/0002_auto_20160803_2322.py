# -*- coding: utf-8 -*-
# Generated by Django 1.9.8 on 2016-08-03 23:22
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('vinculum', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='InputPath',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('input_path', models.TextField()),
            ],
        ),
        migrations.AlterField(
            model_name='remoteresources',
            name='vinculum',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='remote_resources', to='vinculum.Vinculum'),
        ),
        migrations.AddField(
            model_name='inputpath',
            name='remote_resource',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='input_path', to='vinculum.RemoteResources'),
        ),
    ]
