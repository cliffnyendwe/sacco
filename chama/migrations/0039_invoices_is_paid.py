# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('chama', '0038_auto_20160209_1921'),
    ]

    operations = [
        migrations.AddField(
            model_name='invoices',
            name='is_paid',
            field=models.BooleanField(default=False),
        ),
    ]
