# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core_manager', '0017_auto_20160523_2120'),
    ]

    operations = [
        migrations.AlterField(
            model_name='commisiontable',
            name='commission',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='commisiontable',
            name='maximum',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='commisiontable',
            name='minimum',
            field=models.IntegerField(),
        ),
    ]
