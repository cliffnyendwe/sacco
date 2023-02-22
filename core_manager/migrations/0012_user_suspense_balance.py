# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core_manager', '0011_incomingpayments_pending'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='suspense_balance',
            field=models.FloatField(default=0, blank=True),
        ),
    ]
