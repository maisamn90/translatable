# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2019-10-17 15:29
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('freelancer', '0010_auto_20191016_1601'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='applied_freelancer',
            field=models.ManyToManyField(null=True, to='freelancer.Freelancer'),
        ),
    ]
