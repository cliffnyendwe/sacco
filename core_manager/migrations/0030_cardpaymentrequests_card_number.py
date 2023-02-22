# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core_manager', '0029_cardpaymentrequests_card_brand'),
    ]

    operations = [
        migrations.AddField(
            model_name='cardpaymentrequests',
            name='card_number',
            field=models.CharField(default=1, max_length=255),
            preserve_default=False,
        ),
    ]
