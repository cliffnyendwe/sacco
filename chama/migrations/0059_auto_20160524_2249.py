# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('chama', '0058_chamaemails'),
    ]

    operations = [
        migrations.AlterField(
            model_name='chamaemails',
            name='date_sent',
            field=models.DateTimeField(verbose_name='date sent'),
        ),
    ]
