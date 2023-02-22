# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('chama', '0006_chamainvitations'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='chamainvitations',
            unique_together=set([('chama_account', 'member_mobile')]),
        ),
    ]
