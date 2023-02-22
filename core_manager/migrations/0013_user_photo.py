# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import sorl.thumbnail.fields


class Migration(migrations.Migration):

    dependencies = [
        ('core_manager', '0012_user_suspense_balance'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='photo',
            field=sorl.thumbnail.fields.ImageField(default=None, upload_to=b'images/student_photos/%Y/%m'),
        ),
    ]
