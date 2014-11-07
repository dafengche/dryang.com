# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('badminton', '0005_auto_20141106_1629'),
    ]

    operations = [
        migrations.CreateModel(
            name='Contribution',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('contribution_date', models.DateField()),
                ('amount', models.FloatField()),
                ('comment', models.CharField(max_length=255, null=True, blank=True)),
                ('contributor', models.ForeignKey(to='badminton.Player', blank=True)),
            ],
            options={
                'ordering': ['-contribution_date'],
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ContributionType',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255)),
            ],
            options={
                'ordering': ['name'],
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='contribution',
            name='type',
            field=models.ForeignKey(to='badminton.ContributionType'),
            preserve_default=True,
        ),
    ]
