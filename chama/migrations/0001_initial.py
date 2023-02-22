# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ChamaAccount',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('chama_name', models.CharField(max_length=200)),
                ('account_number', models.CharField(max_length=150)),
                ('description', models.TextField(null=True)),
                ('date_created', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date created')),
                ('rotating_amount', models.IntegerField(null=True)),
            ],
            options={
                'verbose_name': 'Chama Account',
                'verbose_name_plural': 'Chama Accounts',
            },
        ),
        migrations.CreateModel(
            name='ChamaContributions',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
            ],
            options={
                'verbose_name': 'Chama Transaction',
                'verbose_name_plural': 'Chama Transactions',
            },
        ),
        migrations.CreateModel(
            name='ChamaMembership',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date_joined')),
                ('current_balance', models.FloatField(default=0, blank=True)),
                ('approved', models.BooleanField(default=False)),
                ('total_approvals', models.IntegerField(default=0, blank=True)),
                ('chama_account', models.ForeignKey(to='chama.ChamaAccount')),
            ],
            options={
                'verbose_name': 'Chama Membership',
                'verbose_name_plural': 'Chama Memberships',
            },
        ),
    ]
