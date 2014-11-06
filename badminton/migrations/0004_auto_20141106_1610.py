# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('badminton', '0003_cost_comment'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cost',
            name='comment',
            field=models.CharField(max_length=255, null=True, blank=True),
        ),
    ]
