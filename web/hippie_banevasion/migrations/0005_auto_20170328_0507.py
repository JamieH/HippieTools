# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-03-28 04:07
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hippie_banevasion', '0004_auto_20170328_0444'),
    ]

    operations = [
        migrations.AlterField(
            model_name='client',
            name='byondversions',
            field=models.ManyToManyField(to='hippie_banevasion.ByondVersion'),
        ),
        migrations.AlterField(
            model_name='client',
            name='last_seen',
            field=models.DateTimeField(blank=True),
        ),
    ]