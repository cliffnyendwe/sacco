# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('promotions', '0005_auto_20161103_1855'),
    ]

    operations = [
        migrations.AddField(
            model_name='promotion',
            name='promotion_start_date',
            field=models.DateTimeField(default=django.utils.timezone.now, verbose_name=b'date created'),
        ),
    ]
