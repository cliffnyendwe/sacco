# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('chama', '0056_closedcircles_date_paid'),
    ]

    operations = [
        migrations.AddField(
            model_name='chamacontributions',
            name='comission_amount',
            field=models.FloatField(default=0, blank=True),
        ),
    ]
