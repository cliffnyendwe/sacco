# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('chama', '0048_chamanotifications_title'),
    ]

    operations = [
        migrations.AlterField(
            model_name='chamanotifications',
            name='title',
            field=models.CharField(max_length=255),
        ),
    ]
