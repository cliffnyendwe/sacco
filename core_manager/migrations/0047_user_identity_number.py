# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core_manager', '0046_remove_user_currency'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='identity_number',
            field=models.CharField(max_length=50, null=True, verbose_name='identity_number', blank=True),
        ),
    ]
