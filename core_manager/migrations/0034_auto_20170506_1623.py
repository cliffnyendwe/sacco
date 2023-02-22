# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('core_manager', '0033_auto_20170506_1609'),
    ]

    operations = [
        migrations.AlterField(
            model_name='clientcard',
            name='date_created',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
