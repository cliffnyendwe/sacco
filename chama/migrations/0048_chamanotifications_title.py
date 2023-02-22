# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('chama', '0047_chamaaccount_is_closed'),
    ]

    operations = [
        migrations.AddField(
            model_name='chamanotifications',
            name='title',
            field=models.TextField(default=1),
            preserve_default=False,
        ),
    ]
