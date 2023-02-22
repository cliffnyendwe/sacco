# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('chama', '0055_auto_20160517_0638'),
    ]

    operations = [
        migrations.AddField(
            model_name='closedcircles',
            name='date_paid',
            field=models.DateTimeField(null=True, verbose_name='date paid', blank=True),
        ),
    ]
