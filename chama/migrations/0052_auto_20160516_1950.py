# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('chama', '0051_auto_20160516_1947'),
    ]

    operations = [
        migrations.AlterField(
            model_name='chamanotifications',
            name='chama_account',
            field=models.ForeignKey(blank=True, to='chama.ChamaAccount', null=True),
        ),
        migrations.AlterField(
            model_name='closedcircles',
            name='chama_account',
            field=models.ForeignKey(to='chama.ChamaAccount', null=True),
        ),
    ]
