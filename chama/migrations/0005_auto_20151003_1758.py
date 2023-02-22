# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('chama', '0004_auto_20151003_1656'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='chamamembership',
            unique_together=set([('chama_account', 'member')]),
        ),
    ]
