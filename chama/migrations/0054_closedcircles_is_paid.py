# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('chama', '0053_closedcircles_closed_by'),
    ]

    operations = [
        migrations.AddField(
            model_name='closedcircles',
            name='is_paid',
            field=models.BooleanField(default=False),
        ),
    ]
