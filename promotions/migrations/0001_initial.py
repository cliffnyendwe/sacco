# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Promotion',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('promotion_name', models.CharField(max_length=200)),
                ('promotion_code', models.CharField(max_length=100, blank=True)),
                ('description', models.TextField(null=True)),
                ('date_created', models.DateTimeField(default=django.utils.timezone.now, verbose_name=b'date created')),
                ('use_promotion_code', models.BooleanField(default=False)),
                ('apply_for_new_subscriptions', models.BooleanField(default=False)),
                ('reward_amount', models.IntegerField(default=0, blank=True)),
                ('reward_percentage', models.IntegerField(default=0, blank=True)),
                ('created_by', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Promotion',
                'verbose_name_plural': 'Promotions',
            },
        ),
    ]
