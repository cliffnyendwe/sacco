# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('chama', '0041_merge'),
    ]

    operations = [
        migrations.AlterField(
            model_name='chamaaccount',
            name='payment_day',
            field=models.IntegerField(default=0, blank=True),
        ),
    ]
