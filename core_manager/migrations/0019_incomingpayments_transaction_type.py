# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core_manager', '0018_auto_20160523_2121'),
    ]

    operations = [
        migrations.AddField(
            model_name='incomingpayments',
            name='transaction_type',
            field=models.CharField(default=1, max_length=255),
            preserve_default=False,
        ),
    ]
