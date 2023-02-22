# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('chama', '0003_auto_20151003_1652'),
    ]

    operations = [
        migrations.AlterField(
            model_name='chamaaccount',
            name='account_number',
            field=models.CharField(unique=True, max_length=150),
        ),
        migrations.AlterField(
            model_name='chamaaccount',
            name='chama_name',
            field=models.CharField(unique=True, max_length=200),
        ),
    ]
