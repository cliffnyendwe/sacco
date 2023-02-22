# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core_manager', '0026_debitcards_is_processed'),
    ]

    operations = [
        migrations.AddField(
            model_name='debitcards',
            name='automatically_deduct',
            field=models.BooleanField(default=False),
        ),
    ]
