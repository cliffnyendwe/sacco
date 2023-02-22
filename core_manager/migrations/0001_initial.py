# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import core_manager.models
import django.utils.timezone
from django.conf import settings
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0006_require_contenttypes_0002'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(null=True, verbose_name='last login', blank=True)),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.SlugField(error_messages={b'unique': 'A user with that username already exists.'}, validators=[django.core.validators.RegexValidator(b'^[\\w.@+-]+$', 'Enter a valid username. This value may contain only letters, numbers and @/./+/-/_ characters.', b'invalid')], help_text='Required. 50 characters or fewer. Letters, digits and @/./+/-/_ only.', unique=True, verbose_name='username')),
                ('other_names', models.CharField(max_length=255, verbose_name='other names', blank=True)),
                ('surname', models.CharField(max_length=30, verbose_name='surname', blank=True)),
                ('gender', models.CharField(blank=True, max_length=6, verbose_name='gender', choices=[(b'male', b'Male'), (b'female', b'Female')])),
                ('email', models.EmailField(max_length=254, unique=True, null=True, verbose_name='email address', blank=True)),
                ('contact_phone', models.CharField(max_length=20, unique=True, null=True, verbose_name='phone number', blank=True)),
                ('profile_picture', models.ImageField(upload_to=b'profile', blank=True)),
                ('is_staff', models.BooleanField(default=False, help_text='Only staff an directly login to the admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user can login to the system. Deactivate users instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('groups', models.ManyToManyField(related_query_name='user', related_name='user_set', to='auth.Group', blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', verbose_name='groups')),
            ],
            options={
                'verbose_name': 'System User',
                'verbose_name_plural': 'System Users',
            },
            managers=[
                ('objects', core_manager.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='PaymentAccount',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('account_number', models.CharField(max_length=150)),
                ('account_name', models.CharField(max_length=150)),
                ('date_created', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date created')),
                ('account_owner', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Payment Account',
                'verbose_name_plural': 'Payment Accounts',
            },
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('product_name', models.CharField(max_length=200)),
                ('product_short_name', models.CharField(max_length=150)),
                ('product_description', models.TextField(null=True)),
                ('date_created', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date created')),
                ('product_owner', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'System Product',
                'verbose_name_plural': 'System Products',
            },
        ),
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('mobile_number', models.CharField(max_length=150)),
                ('amount_paid', models.IntegerField(default=0, blank=True)),
                ('transaction_type', models.CharField(blank=True, max_length=6, verbose_name='transaction_type', choices=[(b'Debit', b'Debit'), (b'Credit', b'Credit')])),
                ('date_paid', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date paid')),
                ('account', models.ForeignKey(to='core_manager.PaymentAccount')),
                ('paid_by', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
                ('product', models.ForeignKey(to='core_manager.Product')),
            ],
            options={
                'verbose_name': 'Transaction',
                'verbose_name_plural': 'Transactions',
            },
        ),
        migrations.AddField(
            model_name='paymentaccount',
            name='product',
            field=models.ForeignKey(to='core_manager.Product'),
        ),
        migrations.AddField(
            model_name='user',
            name='subscriptions',
            field=models.ManyToManyField(to='core_manager.Product', blank=True),
        ),
        migrations.AddField(
            model_name='user',
            name='user_permissions',
            field=models.ManyToManyField(related_query_name='user', related_name='user_set', to='auth.Permission', blank=True, help_text='Specific permissions for this user.', verbose_name='user permissions'),
        ),
    ]
