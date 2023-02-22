# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core_manager', '0037_auto_20170702_0005'),
    ]

    operations = [
        migrations.AddField(
            model_name='circlecurrency',
            name='currency_symbol',
            field=models.CharField(default=1, max_length=150),
            preserve_default=False,
        ),
    ]
