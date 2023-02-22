# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('chama', '0041_chamamembership_last_notification_date'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='chamamembership',
            name='last_notification_date',
        ),
        migrations.AddField(
            model_name='invoices',
            name='last_notification_date',
            field=models.DateField(null=True, blank=True),
        ),
    ]
