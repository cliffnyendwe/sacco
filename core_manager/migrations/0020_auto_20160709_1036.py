# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core_manager', '0019_incomingpayments_transaction_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transaction',
            name='transaction_type',
            field=models.CharField(blank=True, max_length=6, verbose_name='transaction_type', choices=[(b'Debit', b'Debit'), (b'Credit', b'Credit')]),
        ),
    ]
