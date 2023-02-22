# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core_manager', '0010_incomingpayments_processed'),
    ]

    operations = [
        migrations.AddField(
            model_name='incomingpayments',
            name='pending',
            field=models.BooleanField(default=False),
        ),
    ]
