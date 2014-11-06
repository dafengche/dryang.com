# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('badminton', '0002_auto_20141106_1544'),
    ]

    operations = [
        migrations.AddField(
            model_name='cost',
            name='comment',
            field=models.CharField(max_length=255, null=True),
            preserve_default=True,
        ),
    ]
