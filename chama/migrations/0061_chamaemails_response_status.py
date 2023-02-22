# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('chama', '0060_auto_20160524_2250'),
    ]

    operations = [
        migrations.AddField(
            model_name='chamaemails',
            name='response_status',
            field=models.CharField(default=1, max_length=255),
            preserve_default=False,
        ),
    ]
