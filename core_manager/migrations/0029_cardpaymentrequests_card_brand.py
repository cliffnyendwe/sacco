# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core_manager', '0028_auto_20170505_2126'),
    ]

    operations = [
        migrations.AddField(
            model_name='cardpaymentrequests',
            name='card_brand',
            field=models.CharField(default=1, max_length=255),
            preserve_default=False,
        ),
    ]
