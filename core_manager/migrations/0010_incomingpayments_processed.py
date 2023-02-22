# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core_manager', '0009_user_android_device_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='incomingpayments',
            name='processed',
            field=models.BooleanField(default=False),
        ),
    ]
