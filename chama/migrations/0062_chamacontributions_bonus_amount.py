# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('chama', '0061_chamaemails_response_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='chamacontributions',
            name='bonus_amount',
            field=models.FloatField(default=0, blank=True),
        ),
    ]
