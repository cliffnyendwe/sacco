# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('chama', '0018_auto_20151115_1821'),
    ]

    operations = [
        migrations.AddField(
            model_name='chamainvitations',
            name='invited_member',
            field=models.ForeignKey(related_name='invite_member', default=1, to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='chamainvitations',
            name='invited_by',
            field=models.ForeignKey(related_name='invite_by', to=settings.AUTH_USER_MODEL),
        ),
    ]
