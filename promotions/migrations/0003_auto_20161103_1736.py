# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('promotions', '0002_promotion_active'),
    ]

    operations = [
        migrations.AlterField(
            model_name='promotion',
            name='reward_amount',
            field=models.IntegerField(blank=True),
        ),
        migrations.AlterField(
            model_name='promotion',
            name='reward_percentage',
            field=models.IntegerField(blank=True),
        ),
    ]
