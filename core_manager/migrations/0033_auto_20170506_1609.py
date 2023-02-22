# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core_manager', '0032_clientcard'),
    ]

    operations = [
        migrations.AddField(
            model_name='clientcard',
            name='date_created',
            field=models.CharField(default=1, max_length=255),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='clientcard',
            name='remember_card_details',
            field=models.BooleanField(default=False),
        ),
    ]
