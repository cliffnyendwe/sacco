# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('chama', '0025_auto_20151130_1715'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='chamaaccount',
            name='total_contribution',
        ),
    ]
