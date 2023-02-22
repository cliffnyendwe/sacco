# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('chama', '0023_auto_20151118_1756'),
    ]

    operations = [
        migrations.AddField(
            model_name='chamaaccount',
            name='total_contribution',
            field=models.FloatField(null=True),
        ),
    ]
