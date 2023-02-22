# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('chama', '0010_chamacontributions_paid_by'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='chamacontributions',
            options={'verbose_name': 'Chama Contribution', 'verbose_name_plural': 'Chama Contributions'},
        ),
    ]
