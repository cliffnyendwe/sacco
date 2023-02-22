# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('chama', '0021_auto_20151115_1859'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='chamamembership',
            name='total_approvals',
        ),
    ]
