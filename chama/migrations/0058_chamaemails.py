# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('chama', '0057_chamacontributions_comission_amount'),
    ]

    operations = [
        migrations.CreateModel(
            name='ChamaEmails',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('mail_subject', models.CharField(max_length=255)),
                ('mail_message', models.TextField()),
                ('from_address', models.CharField(max_length=255)),
                ('to_address', models.CharField(max_length=255)),
                ('sent', models.BooleanField(default=False)),
                ('date_created', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date created')),
                ('date_sent', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date sent')),
            ],
            options={
                'verbose_name': 'Chama Emails',
                'verbose_name_plural': 'Chama Emails',
            },
        ),
    ]
