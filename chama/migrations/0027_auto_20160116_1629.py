# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('chama', '0026_remove_chamaaccount_total_contribution'),
    ]

    operations = [
        migrations.AlterField(
            model_name='chamacontributions',
            name='amount_paid',
            field=models.FloatField(default=0, blank=True),
        ),
    ]
