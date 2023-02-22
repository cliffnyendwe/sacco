# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('chama', '0016_auto_20151115_1816'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='memberappprovals',
            unique_together=set([]),
        ),
        migrations.RemoveField(
            model_name='memberappprovals',
            name='chama_account',
        ),
        migrations.RemoveField(
            model_name='memberappprovals',
            name='invited_member',
        ),
        migrations.DeleteModel(
            name='MemberAppprovals',
        ),
    ]
