# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('chama', '0067_auto_20171006_0648'),
    ]

    operations = [
        migrations.RenameField(
            model_name='surveylist',
            old_name='surver_user',
            new_name='survey_user',
        ),
    ]
