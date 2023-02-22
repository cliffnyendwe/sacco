# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core_manager', '0016_user_reset_code'),
    ]

    operations = [
        migrations.CreateModel(
            name='CommisionTable',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('minimum', models.IntegerField(max_length=150)),
                ('maximum', models.IntegerField(max_length=150)),
                ('commission', models.IntegerField(max_length=150)),
            ],
            options={
                'verbose_name': 'Commision Table',
                'verbose_name_plural': 'Commision Table',
            },
        ),
        migrations.AlterField(
            model_name='transaction',
            name='transaction_type',
            field=models.CharField(blank=True, max_length=6, verbose_name='transaction_type', choices=[(b'Debit', b'Debit'), (b'11111', b'Credit')]),
        ),
    ]
