# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core_manager', '0007_remove_paymentaccount_account_owner'),
    ]

    operations = [
        migrations.CreateModel(
            name='IncomingPayments',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('transaction_id', models.CharField(max_length=255)),
                ('orig', models.CharField(max_length=255)),
                ('dest', models.CharField(max_length=255)),
                ('tstamp', models.CharField(max_length=255)),
                ('text', models.CharField(unique=True, max_length=255)),
                ('customer_id', models.CharField(max_length=255)),
                ('mpesa_code', models.CharField(max_length=255)),
                ('mpesa_acc', models.CharField(max_length=255)),
                ('mpesa_msisdn', models.CharField(max_length=255)),
                ('mpesa_trx_date', models.CharField(max_length=255)),
                ('mpesa_trx_time', models.CharField(max_length=255)),
                ('mpesa_amt', models.CharField(max_length=255)),
                ('mpesa_sender', models.CharField(max_length=255)),
                ('business_number', models.CharField(max_length=255)),
                ('source', models.CharField(max_length=255)),
            ],
        ),
    ]
