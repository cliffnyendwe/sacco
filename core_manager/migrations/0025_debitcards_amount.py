# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core_manager', '0024_auto_20170406_2234'),
    ]

    operations = [
        migrations.AddField(
            model_name='debitcards',
            name='amount',
            field=models.CharField(default=1, max_length=255),
            preserve_default=False,
        ),
    ]
