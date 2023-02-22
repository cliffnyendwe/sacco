# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core_manager', '0002_auto_20151003_1552'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='surname',
        ),
        migrations.AddField(
            model_name='user',
            name='first_name',
            field=models.CharField(max_length=30, verbose_name='first name', blank=True),
        ),
    ]
