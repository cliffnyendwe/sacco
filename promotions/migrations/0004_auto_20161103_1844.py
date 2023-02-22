# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('promotions', '0003_auto_20161103_1736'),
    ]

    operations = [
        migrations.AlterField(
            model_name='promotion',
            name='reward_amount',
            field=models.IntegerField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='promotion',
            name='use_promotion_code',
            field=models.BooleanField(default=False, help_text=b'Used for promotions that utilize promo codes'),
        ),
    ]
