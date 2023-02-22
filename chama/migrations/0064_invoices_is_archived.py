# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('chama', '0063_chamamembership_is_active'),
    ]

    operations = [
        migrations.AddField(
            model_name='invoices',
            name='is_archived',
            field=models.BooleanField(default=False),
        ),
    ]
