# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('chama', '0028_invoices'),
    ]

    operations = [
        migrations.AlterField(
            model_name='invoices',
            name='due_date',
            field=models.DateField(default=django.utils.timezone.now),
        ),
    ]
