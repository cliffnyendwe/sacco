# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('chama', '0039_invoices_is_paid'),
    ]

    operations = [
        migrations.AlterField(
            model_name='chamacontributions',
            name='mobile_number',
            field=models.CharField(max_length=150, null=True, blank=True),
        ),
    ]
