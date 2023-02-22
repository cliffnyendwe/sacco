# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('chama', '0059_auto_20160524_2249'),
    ]

    operations = [
        migrations.AlterField(
            model_name='chamaemails',
            name='date_sent',
            field=models.DateTimeField(null=True, verbose_name='date sent'),
        ),
    ]
