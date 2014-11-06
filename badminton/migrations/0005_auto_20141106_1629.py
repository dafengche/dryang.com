# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('badminton', '0004_auto_20141106_1610'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='cost',
            options={'ordering': ['-cost_date']},
        ),
        migrations.AlterModelOptions(
            name='costtype',
            options={'ordering': ['name']},
        ),
        migrations.AlterModelOptions(
            name='record',
            options={'ordering': ['-play_date']},
        ),
        migrations.AlterField(
            model_name='record',
            name='comment',
            field=models.CharField(max_length=511, null=True, blank=True),
        ),
    ]
