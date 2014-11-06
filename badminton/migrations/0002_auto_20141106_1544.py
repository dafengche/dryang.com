# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0001_initial'),
        ('badminton', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='player',
            name='user',
        ),
        migrations.DeleteModel(
            name='Player',
        ),
        migrations.CreateModel(
            name='Player',
            fields=[
            ],
            options={
                'ordering': ['first_name'],
                'proxy': True,
            },
            bases=('auth.user',),
        ),
    ]
