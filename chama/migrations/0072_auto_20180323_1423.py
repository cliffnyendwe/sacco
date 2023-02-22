# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('chama', '0071_merge'),
    ]

    operations = [
        migrations.AddField(
            model_name='chamaaccount',
            name='payment_cycle_choice',
            field=models.CharField(max_length=150, null=True),
        ),
        migrations.AddField(
            model_name='chamaaccount',
            name='payment_cycle_option',
            field=models.CharField(max_length=150, null=True),
        ),
        migrations.AlterField(
            model_name='chamaaccount',
            name='payment_day',
            field=models.CharField(max_length=150, null=True),
        ),
        migrations.AlterField(
            model_name='closedcircles',
            name='payment_option',
            field=models.CharField(blank=True, max_length=255, null=True, choices=[(b'BANK', 'Bank'), (b'MPESA', 'M-Pesa')]),
        ),
    ]
