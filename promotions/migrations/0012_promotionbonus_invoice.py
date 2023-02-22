# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('chama', '0062_chamacontributions_bonus_amount'),
        ('promotions', '0011_auto_20161103_2220'),
    ]

    operations = [
        migrations.AddField(
            model_name='promotionbonus',
            name='invoice',
            field=models.ForeignKey(to='chama.Invoices', null=True),
        ),
    ]
