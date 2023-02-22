# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('chama', '0017_auto_20151115_1820'),
    ]

    operations = [
        migrations.CreateModel(
            name='MemberAppprovals',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('approved', models.BooleanField(default=False)),
                ('chama_account', models.ForeignKey(to='chama.ChamaAccount')),
                ('invited_member', models.ForeignKey(related_name='invited_member', to=settings.AUTH_USER_MODEL)),
                ('member_to_approve', models.ForeignKey(related_name='member_to_approve', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Chama Member Approval',
                'verbose_name_plural': 'Chama Member Approvals',
            },
        ),
        migrations.AlterUniqueTogether(
            name='memberappprovals',
            unique_together=set([('invited_member', 'chama_account', 'member_to_approve')]),
        ),
    ]
