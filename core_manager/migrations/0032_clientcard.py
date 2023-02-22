# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('core_manager', '0031_cardpaymentrequests_remember_card_details'),
    ]

    operations = [
        migrations.CreateModel(
            name='ClientCard',
            fields=[
                ('card_owner', models.OneToOneField(primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('customer_id', models.CharField(max_length=255)),
                ('card_number', models.CharField(max_length=255)),
                ('automatically_deduct', models.BooleanField(default=False)),
            ],
            options={
                'verbose_name': 'Client Card',
                'verbose_name_plural': 'Client Cards',
            },
        ),
    ]
