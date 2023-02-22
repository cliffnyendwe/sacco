# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core_manager', '0049_auto_20180525_1125'),
    ]

    operations = [
        migrations.AddField(
            model_name='circlecurrency',
            name='is_active',
            field=models.BooleanField(default=True, verbose_name='active'),
        ),
    ]
