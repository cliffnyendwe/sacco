# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core_manager', '0035_pesapaltransactions_pesapaltransactionusers'),
    ]

    operations = [
        migrations.CreateModel(
            name='Currency',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('currency_code', models.CharField(max_length=150)),
                ('currency_name', models.CharField(max_length=150)),
            ],
            options={
                'verbose_name': 'Currency',
                'verbose_name_plural': 'Currencies',
            },
        ),
    ]
