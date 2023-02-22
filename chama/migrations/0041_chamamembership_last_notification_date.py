# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('chama', '0040_auto_20160209_2047'),
    ]

    operations = [
        migrations.AddField(
            model_name='chamamembership',
            name='last_notification_date',
            field=models.DateField(null=True, blank=True),
        ),
    ]
