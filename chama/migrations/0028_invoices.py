# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('chama', '0027_auto_20160116_1629'),
    ]

    operations = [
        migrations.CreateModel(
            name='Invoices',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('amount_required', models.FloatField(default=0, blank=True)),
                ('due_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('chama_account', models.ForeignKey(to='chama.ChamaAccount')),
                ('payer', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Invoice',
                'verbose_name_plural': 'Invoices',
            },
        ),
    ]
