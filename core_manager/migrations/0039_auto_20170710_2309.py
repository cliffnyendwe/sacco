# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core_manager', '0038_circlecurrency_currency_symbol'),
    ]

    operations = [
        migrations.AddField(
            model_name='circlecurrency',
            name='conversion_rate',
            field=models.FloatField(default=0, blank=True),
        ),
        migrations.AddField(
            model_name='circlecurrency',
            name='is_base_currency',
            field=models.BooleanField(default=False),
        ),
    ]
