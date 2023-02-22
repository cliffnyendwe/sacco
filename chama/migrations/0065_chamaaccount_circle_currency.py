# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core_manager', '0037_auto_20170702_0005'),
        ('chama', '0064_invoices_is_archived'),
    ]

    operations = [
        migrations.AddField(
            model_name='chamaaccount',
            name='circle_currency',
            field=models.OneToOneField(null=True, to='core_manager.CircleCurrency'),
        ),
    ]
