# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('promotions', '0007_auto_20161103_1931'),
    ]

    operations = [
        migrations.AlterField(
            model_name='promotion',
            name='reward_amount',
            field=models.IntegerField(default=0, blank=True),
        ),
        migrations.AlterField(
            model_name='promotion',
            name='reward_percentage',
            field=models.IntegerField(default=0, blank=True),
        ),
    ]
