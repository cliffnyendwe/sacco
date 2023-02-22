# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core_manager', '0036_currency'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Currency',
            new_name='CircleCurrency',
        ),
        migrations.AlterModelOptions(
            name='circlecurrency',
            options={'verbose_name': 'Circle Currency', 'verbose_name_plural': 'Circle Currencies'},
        ),
    ]
