# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('chama', '0013_chamainvitations_invite_accepted'),
    ]

    operations = [
        migrations.AddField(
            model_name='chamainvitations',
            name='invite_rejejcted',
            field=models.BooleanField(default=False),
        ),
    ]
