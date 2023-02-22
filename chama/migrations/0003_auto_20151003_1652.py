# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('chama', '0002_auto_20151003_1543'),
    ]

    operations = [
        migrations.AlterField(
            model_name='chamaaccount',
            name='rotating_amount',
            field=models.FloatField(null=True),
        ),
    ]
