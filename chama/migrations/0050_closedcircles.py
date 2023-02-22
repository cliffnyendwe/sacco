# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('chama', '0049_auto_20160501_1333'),
    ]

    operations = [
        migrations.CreateModel(
            name='ClosedCircles',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('bank_name', models.CharField(max_length=255)),
                ('account_name', models.CharField(max_length=255)),
                ('payment_option', models.CharField(max_length=255)),
                ('bank_branch', models.CharField(max_length=255)),
                ('swift', models.CharField(max_length=255)),
                ('mpesa_number', models.CharField(max_length=255)),
                ('national_id', models.CharField(max_length=255)),
                ('comments', models.TextField()),
                ('date_closed', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date closed')),
                ('chama_account', models.ForeignKey(blank=True, to='chama.ChamaAccount', null=True)),
            ],
            options={
                'verbose_name': 'Closed Circle',
                'verbose_name_plural': 'Closed Circle',
            },
        ),
    ]
