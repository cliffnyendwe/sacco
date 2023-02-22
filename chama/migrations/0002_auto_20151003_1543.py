# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('chama', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('core_manager', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='chamamembership',
            name='member',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='chamacontributions',
            name='chama_account',
            field=models.ForeignKey(to='chama.ChamaAccount'),
        ),
        migrations.AddField(
            model_name='chamacontributions',
            name='contribution',
            field=models.ForeignKey(to='core_manager.Transaction'),
        ),
        migrations.AddField(
            model_name='chamaaccount',
            name='administrator',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='chamaaccount',
            name='contributions',
            field=models.ManyToManyField(related_name='chama_contributions', through='chama.ChamaContributions', to='core_manager.Transaction'),
        ),
        migrations.AddField(
            model_name='chamaaccount',
            name='members',
            field=models.ManyToManyField(related_name='chama_member', through='chama.ChamaMembership', to=settings.AUTH_USER_MODEL),
        ),
    ]
