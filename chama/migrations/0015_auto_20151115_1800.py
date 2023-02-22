# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('chama', '0014_chamainvitations_invite_rejejcted'),
    ]

    operations = [
        migrations.RenameField(
            model_name='chamainvitations',
            old_name='invite_rejejcted',
            new_name='invite_rejected',
        ),
        migrations.AlterUniqueTogether(
            name='chamainvitations',
            unique_together=set([]),
        ),
    ]
