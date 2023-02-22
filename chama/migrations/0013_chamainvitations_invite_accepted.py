# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('chama', '0012_chamainvitations_notified'),
    ]

    operations = [
        migrations.AddField(
            model_name='chamainvitations',
            name='invite_accepted',
            field=models.BooleanField(default=False),
        ),
    ]
