# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('chama', '0024_chamaaccount_total_contribution'),
    ]

    operations = [
        migrations.AlterField(
            model_name='chamaaccount',
            name='rotating_amount',
            field=models.FloatField(default=0, blank=True),
        ),
        migrations.AlterField(
            model_name='chamaaccount',
            name='total_contribution',
            field=models.FloatField(default=0, blank=True),
        ),
    ]
