# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('core_manager', '0027_debitcards_automatically_deduct'),
    ]

    operations = [
        migrations.CreateModel(
            name='CardPaymentRequests',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('token_id', models.CharField(max_length=255)),
                ('live_mode', models.CharField(max_length=255)),
                ('token_used', models.CharField(max_length=255)),
                ('date_created', models.CharField(max_length=255)),
                ('trans_type', models.CharField(max_length=255)),
                ('amount', models.CharField(max_length=255)),
                ('is_processed', models.BooleanField(default=False)),
                ('automatically_deduct', models.BooleanField(default=False)),
                ('card_owner', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Card Payment Request',
                'verbose_name_plural': 'Card Payment Requests',
            },
        ),
        migrations.AlterUniqueTogether(
            name='debitcards',
            unique_together=set([]),
        ),
        migrations.RemoveField(
            model_name='debitcards',
            name='card_owner',
        ),
        migrations.DeleteModel(
            name='DebitCards',
        ),
        migrations.AlterUniqueTogether(
            name='cardpaymentrequests',
            unique_together=set([('token_id', 'card_owner')]),
        ),
    ]
