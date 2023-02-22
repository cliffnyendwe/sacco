# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core_manager', '0045_remove_incomingpayments_currency'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='currency',
        ),
    ]
