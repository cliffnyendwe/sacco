# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core_manager', '0023_debitcards_card_owner'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='debitcards',
            options={'verbose_name': 'Debit Card', 'verbose_name_plural': 'Debit Cards'},
        ),
        migrations.AlterUniqueTogether(
            name='debitcards',
            unique_together=set([('token_id', 'card_owner')]),
        ),
    ]
