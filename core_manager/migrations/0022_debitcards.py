# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core_manager', '0021_auto_20160709_1040'),
    ]

    operations = [
        migrations.CreateModel(
            name='DebitCards',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('token_id', models.CharField(max_length=255)),
                ('live_mode', models.CharField(max_length=255)),
                ('token_used', models.CharField(max_length=255)),
                ('date_created', models.CharField(max_length=255)),
                ('trans_type', models.CharField(max_length=255)),
            ],
        ),
    ]
