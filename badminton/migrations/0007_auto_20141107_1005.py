# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('badminton', '0006_auto_20141107_0951'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contribution',
            name='contributor',
            field=models.ForeignKey(blank=True, to='badminton.Player', null=True),
        ),
    ]
