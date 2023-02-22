# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('chama', '0068_auto_20171006_0652'),
    ]

    operations = [
        migrations.CreateModel(
            name='InactiveMembership',
            fields=[
            ],
            options={
                'default_permissions': ('add', 'change', 'delete', 'view'),
                'verbose_name': 'Inactive Membership',
                'proxy': True,
                'verbose_name_plural': 'Inactive Memberships',
            },
            bases=('chama.chamamembership',),
        ),
    ]
