# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('chama', '0050_closedcircles'),
    ]

    operations = [
        migrations.AddField(
            model_name='closedcircles',
            name='account_number',
            field=models.CharField(max_length=255, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='chamanotifications',
            name='chama_account',
            field=models.ForeignKey(default=1, to='chama.ChamaAccount'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='closedcircles',
            name='account_name',
            field=models.CharField(max_length=255, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='closedcircles',
            name='bank_branch',
            field=models.CharField(max_length=255, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='closedcircles',
            name='bank_name',
            field=models.CharField(max_length=255, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='closedcircles',
            name='mpesa_number',
            field=models.CharField(max_length=255, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='closedcircles',
            name='national_id',
            field=models.CharField(max_length=255, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='closedcircles',
            name='payment_option',
            field=models.CharField(max_length=255, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='closedcircles',
            name='swift',
            field=models.CharField(max_length=255, null=True, blank=True),
        ),
    ]
