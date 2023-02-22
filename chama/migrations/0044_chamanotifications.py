# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('chama', '0043_merge'),
    ]

    operations = [
        migrations.CreateModel(
            name='ChamaNotifications',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('message', models.TextField()),
                ('sent', models.BooleanField(default=False)),
                ('date_created', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date created')),
                ('total_recipients', models.IntegerField(default=0, blank=True)),
                ('chama_account', models.ForeignKey(blank=True, to='chama.ChamaAccount', null=True)),
                ('chama_user', models.ForeignKey(related_name='recipient', blank=True, to=settings.AUTH_USER_MODEL, null=True)),
                ('sent_by', models.ForeignKey(related_name='sent_by', blank=True, to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
                'verbose_name': 'Chama Notifications',
                'verbose_name_plural': 'Chama Notifications',
            },
        ),
    ]
