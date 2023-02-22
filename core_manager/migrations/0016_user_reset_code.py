# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core_manager', '0015_auto_20160419_1852'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='reset_code',
            field=models.CharField(max_length=20, null=True, verbose_name='pasword reset code', blank=True),
        ),
    ]
