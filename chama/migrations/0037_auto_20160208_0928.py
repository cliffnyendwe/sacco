# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('chama', '0036_auto_20160206_1913'),
    ]

    operations = [
        migrations.AlterField(
            model_name='chamaaccount',
            name='chama_name',
            field=models.CharField(max_length=200),
        ),
    ]
