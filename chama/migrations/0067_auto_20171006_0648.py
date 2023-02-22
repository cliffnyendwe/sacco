# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import core_manager.models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('core_manager', '0046_remove_user_currency'),
        ('chama', '0066_auto_20170702_0038'),
    ]

    operations = [
        migrations.CreateModel(
            name='NoticeList',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('unpaid_invoices', models.IntegerField(default=0, blank=True)),
                ('delivered', models.BooleanField(default=False)),
            ],
            options={
                'default_permissions': ('add', 'change', 'delete', 'view'),
                'verbose_name': 'Notice List',
                'verbose_name_plural': 'Notice List',
            },
        ),
        migrations.CreateModel(
            name='SurveyList',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('unpaid_invoices', models.IntegerField(default=0, blank=True)),
                ('completed', models.BooleanField(default=False)),
            ],
            options={
                'default_permissions': ('add', 'change', 'delete', 'view'),
                'verbose_name': 'Survey List',
                'verbose_name_plural': 'Survey List',
            },
        ),
        migrations.CreateModel(
            name='UnpaidInvoices',
            fields=[
            ],
            options={
                'default_permissions': ('add', 'change', 'delete', 'view'),
                'verbose_name': 'Unpaid Invoice',
                'proxy': True,
                'verbose_name_plural': 'Unpaid Invoices',
            },
            bases=('core_manager.user',),
            managers=[
                ('objects', core_manager.models.UserManager()),
            ],
        ),
        migrations.AddField(
            model_name='invoices',
            name='total_reminders',
            field=models.IntegerField(default=0, blank=True),
        ),
        migrations.AddField(
            model_name='surveylist',
            name='surver_user',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='noticelist',
            name='notice_user',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
        ),
    ]
