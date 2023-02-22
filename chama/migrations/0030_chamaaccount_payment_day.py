# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('chama', '0029_auto_20160206_1757'),
    ]

    operations = [
        migrations.AddField(
            model_name='chamaaccount',
            name='payment_day',
            field=models.IntegerField(default=0, blank=True),
        ),
    ]
