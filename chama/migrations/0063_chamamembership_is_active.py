# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('chama', '0062_chamacontributions_bonus_amount'),
    ]

    operations = [
        migrations.AddField(
            model_name='chamamembership',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
    ]
