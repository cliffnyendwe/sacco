# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core_manager', '0008_incomingpayments'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='android_device_id',
            field=models.CharField(max_length=200, blank=True),
        ),
    ]
