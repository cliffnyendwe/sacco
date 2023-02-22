# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('promotions', '0008_auto_20161103_2154'),
    ]

    operations = [
        migrations.CreateModel(
            name='PromotionBonus',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('bonus_amount', models.FloatField(default=0, blank=True)),
                ('circle_member', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
                ('promotion', models.ForeignKey(to='promotions.Promotion')),
            ],
        ),
    ]
