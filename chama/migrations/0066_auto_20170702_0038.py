# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('chama', '0065_chamaaccount_circle_currency'),
    ]

    operations = [
        migrations.AlterField(
            model_name='chamaaccount',
            name='circle_currency',
            field=models.ForeignKey(to='core_manager.CircleCurrency', null=True),
        ),
    ]
