# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('core_manager', '0034_auto_20170506_1623'),
    ]

    operations = [
        migrations.CreateModel(
            name='PesaPalTransactions',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('currency', models.CharField(max_length=255)),
                ('amount', models.FloatField(default=0, blank=True)),
                ('status', models.CharField(max_length=255)),
                ('reference_number', models.CharField(max_length=255)),
                ('tracking_id', models.CharField(max_length=255)),
                ('payment_method', models.CharField(max_length=255)),
                ('user_id', models.CharField(max_length=255)),
                ('member_code', models.CharField(max_length=255)),
                ('date_initiated', models.DateTimeField(default=django.utils.timezone.now)),
                ('is_processed', models.BooleanField(default=False)),
            ],
            options={
                'verbose_name': 'PesaPal Transaction',
                'verbose_name_plural': 'PesaPal Transactions',
            },
        ),
        migrations.CreateModel(
            name='PesaPalTransactionUsers',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('first_name', models.CharField(max_length=255)),
                ('last_name', models.CharField(max_length=255)),
                ('email', models.CharField(max_length=255)),
                ('phone_number', models.CharField(max_length=255)),
            ],
            options={
                'verbose_name': 'PesaPal Transaction User',
                'verbose_name_plural': 'PesaPal Transaction Users',
            },
        ),
    ]
