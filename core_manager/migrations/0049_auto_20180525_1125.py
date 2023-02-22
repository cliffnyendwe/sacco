# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core_manager', '0048_auto_20171020_1219'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='incomingpayments',
            options={'verbose_name': 'Incoming Payment', 'verbose_name_plural': 'Incoming Payments'},
        ),
        migrations.AddField(
            model_name='incomingpayments',
            name='confirmation_reference',
            field=models.CharField(max_length=255, blank=True),
        ),
        migrations.AddField(
            model_name='incomingpayments',
            name='currency_code',
            field=models.CharField(default='KES', max_length=255),
            preserve_default=False,
        ),
        migrations.AlterUniqueTogether(
            name='incomingpayments',
            unique_together=set([('transaction_id', 'source')]),
        ),
    ]
