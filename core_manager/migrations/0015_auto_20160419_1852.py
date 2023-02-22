# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import sorl.thumbnail.fields


class Migration(migrations.Migration):

    dependencies = [
        ('core_manager', '0014_auto_20160419_1116'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='photo',
            field=sorl.thumbnail.fields.ImageField(default=None, upload_to=b'images/member_photos/%Y/%m', blank=True),
        ),
    ]
