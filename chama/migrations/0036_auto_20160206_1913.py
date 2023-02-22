# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('chama', '0035_chamamembership_last_invoice_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='chamamembership',
            name='last_invoice_date',
            field=models.DateField(null=True, blank=True),
        ),
    ]
