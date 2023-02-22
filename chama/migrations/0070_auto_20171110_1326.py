# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('chama', '0069_inactivemembership'),
    ]

    operations = [
        migrations.AlterField(
            model_name='closedcircles',
            name='payment_option',
            field=models.CharField(blank=True, max_length=255, null=True, choices=[(1, 'Not relevant'), (2, 'Review'), (3, 'Maybe relevant'), (4, 'Relevant'), (5, 'Leading candidate')]),
        ),
    ]
