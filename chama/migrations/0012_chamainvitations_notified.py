# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('chama', '0011_auto_20151112_1901'),
    ]

    operations = [
        migrations.AddField(
            model_name='chamainvitations',
            name='notified',
            field=models.BooleanField(default=False),
        ),
    ]
