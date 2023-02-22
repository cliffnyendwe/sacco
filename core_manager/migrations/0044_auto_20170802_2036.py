# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core_manager', '0043_auto_20170802_1100'),
    ]

    operations = [
        migrations.AlterField(
            model_name='incomingpayments',
            name='currency',
            field=models.ForeignKey(default=2, to='core_manager.CircleCurrency', null=True),
        ),
    ]
