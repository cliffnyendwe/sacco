# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core_manager', '0005_remove_user_profile_picture'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='product_owner',
        ),
        migrations.RemoveField(
            model_name='paymentaccount',
            name='product',
        ),
        migrations.RemoveField(
            model_name='transaction',
            name='product',
        ),
        migrations.RemoveField(
            model_name='user',
            name='subscriptions',
        ),
        migrations.DeleteModel(
            name='Product',
        ),
    ]
