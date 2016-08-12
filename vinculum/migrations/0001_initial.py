# -*- coding: utf-8 -*-
# Generated by Django 1.9.8 on 2016-08-11 21:06
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='InputOutputPath',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('input_path', models.TextField()),
                ('output_path', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='RemoteResources',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('authentication_behavior', models.CharField(blank=True, default='', max_length=100)),
                ('remote_resource_path', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Vinculum',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('title', models.CharField(blank=True, default='', max_length=100)),
                ('root_path', models.CharField(blank=True, max_length=1024)),
                ('task_id', models.PositiveIntegerField(blank=True, default=0)),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='vinculum', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ('created',),
            },
        ),
        migrations.AddField(
            model_name='remoteresources',
            name='vinculum',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='remote_resources', to='vinculum.Vinculum'),
        ),
        migrations.AddField(
            model_name='inputoutputpath',
            name='remote_resource',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='io_paths', to='vinculum.RemoteResources'),
        ),
    ]
