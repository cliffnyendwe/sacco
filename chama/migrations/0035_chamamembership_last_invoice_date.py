# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('chama', '0034_auto_20160206_1853'),
    ]

    operations = [
        migrations.AddField(
            model_name='chamamembership',
            name='last_invoice_date',
            field=models.DateTimeField(null=True, blank=True),
        ),
    ]
