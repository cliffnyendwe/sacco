# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core_manager', '0020_auto_20160709_1036'),
    ]

    operations = [
        migrations.AlterField(
            model_name='incomingpayments',
            name='text',
            field=models.CharField(max_length=255),
        ),
    ]
