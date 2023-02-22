# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('chama', '0019_auto_20151115_1855'),
    ]

    operations = [
        migrations.AlterField(
            model_name='chamainvitations',
            name='invited_member',
            field=models.ForeignKey(related_name='invite_member', blank=True, to=settings.AUTH_USER_MODEL),
        ),
    ]
