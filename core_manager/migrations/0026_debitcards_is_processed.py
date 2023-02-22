# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core_manager', '0025_debitcards_amount'),
    ]

    operations = [
        migrations.AddField(
            model_name='debitcards',
            name='is_processed',
            field=models.BooleanField(default=False),
        ),
    ]
