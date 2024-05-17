# -*- coding: utf-8 -*-
# Generated by Django 1.11.17 on 2022-12-15 04:25
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('library_app', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Books',
            fields=[
                ('b_id', models.IntegerField(primary_key=True, serialize=False)),
                ('book_name', models.CharField(max_length=255)),
                ('author_name', models.CharField(max_length=255)),
                ('publication', models.CharField(max_length=255)),
                ('year', models.CharField(max_length=255)),
                ('rack_number', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Request',
            fields=[
                ('r_id', models.IntegerField(primary_key=True, serialize=False)),
                ('username', models.CharField(max_length=255)),
                ('password', models.CharField(max_length=255)),
                ('name', models.CharField(max_length=255)),
                ('address', models.CharField(max_length=255)),
                ('age', models.CharField(max_length=255)),
                ('email', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('u_id', models.IntegerField(primary_key=True, serialize=False)),
                ('username', models.CharField(max_length=255)),
                ('password', models.CharField(max_length=255)),
                ('name', models.CharField(max_length=255)),
                ('address', models.CharField(max_length=255)),
                ('age', models.CharField(max_length=255)),
                ('email', models.CharField(max_length=255)),
            ],
        ),
        migrations.DeleteModel(
            name='Requests',
        ),
        migrations.DeleteModel(
            name='Users',
        ),
    ]