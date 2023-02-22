# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('chama', '0044_chamanotifications'),
    ]

    operations = [
        migrations.RenameField(
            model_name='chamanotifications',
            old_name='chama_user',
            new_name='recipient',
        ),
    ]
