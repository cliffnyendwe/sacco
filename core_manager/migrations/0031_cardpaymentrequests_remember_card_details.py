# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core_manager', '0030_cardpaymentrequests_card_number'),
    ]

    operations = [
        migrations.AddField(
            model_name='cardpaymentrequests',
            name='remember_card_details',
            field=models.BooleanField(default=False),
        ),
    ]
