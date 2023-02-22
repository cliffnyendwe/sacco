# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core_manager', '0004_user_member_code'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='profile_picture',
        ),
    ]
