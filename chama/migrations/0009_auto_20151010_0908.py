# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('chama', '0008_chamainvitations_invited_by'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='chamacontributions',
            name='contribution',
        ),
        migrations.AddField(
            model_name='chamacontributions',
            name='amount_paid',
            field=models.IntegerField(default=0, blank=True),
        ),
        migrations.AddField(
            model_name='chamacontributions',
            name='date_paid',
            field=models.DateTimeField(default=django.utils.timezone.now, verbose_name='date paid'),
        ),
        migrations.AddField(
            model_name='chamacontributions',
            name='mobile_number',
            field=models.CharField(default=1, max_length=150),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='chamacontributions',
            name='transaction_type',
            field=models.CharField(blank=True, max_length=6, verbose_name='transaction_type', choices=[(b'Debit', b'Debit'), (b'Credit', b'Credit')]),
        ),
        migrations.RemoveField(
            model_name='chamaaccount',
            name='contributions',
        ),
        migrations.AddField(
            model_name='chamaaccount',
            name='contributions',
            field=models.ForeignKey(to='chama.ChamaContributions', null=True),
        ),
    ]
