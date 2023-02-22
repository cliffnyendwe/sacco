# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('chama', '0054_closedcircles_is_paid'),
    ]

    operations = [
        migrations.AlterField(
            model_name='closedcircles',
            name='comments',
            field=models.TextField(blank=True),
        ),
    ]
