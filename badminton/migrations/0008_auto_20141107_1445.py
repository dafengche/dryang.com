# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('badminton', '0007_auto_20141107_1005'),
    ]

    operations = [
        migrations.AddField(
            model_name='contribution',
            name='financial_year',
            field=models.IntegerField(default=2014),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='cost',
            name='financial_year',
            field=models.IntegerField(default=2014),
            preserve_default=False,
        ),
    ]
