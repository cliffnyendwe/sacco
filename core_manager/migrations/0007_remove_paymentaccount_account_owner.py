# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core_manager', '0006_auto_20151112_1842'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='paymentaccount',
            name='account_owner',
        ),
    ]
