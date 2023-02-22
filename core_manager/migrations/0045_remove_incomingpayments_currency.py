# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core_manager', '0044_auto_20170802_2036'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='incomingpayments',
            name='currency',
        ),
    ]
