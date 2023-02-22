# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('chama', '0046_notificationlog'),
    ]

    operations = [
        migrations.AddField(
            model_name='chamaaccount',
            name='is_closed',
            field=models.IntegerField(default=0, blank=True),
        ),
    ]
