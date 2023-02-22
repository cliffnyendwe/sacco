# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('chama', '0037_auto_20160208_0928'),
    ]

    operations = [
        migrations.AlterField(
            model_name='invoices',
            name='due_date',
            field=models.DateField(),
        ),
    ]
