# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('chama', '0005_auto_20151003_1758'),
    ]

    operations = [
        migrations.CreateModel(
            name='ChamaInvitations',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('member_mobile', models.CharField(max_length=100)),
                ('chama_account', models.ForeignKey(to='chama.ChamaAccount')),
            ],
        ),
    ]
