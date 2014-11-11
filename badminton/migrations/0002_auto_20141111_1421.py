# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0001_initial'),
        ('badminton', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Contribution',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('contribution_date', models.DateField()),
                ('amount', models.FloatField()),
                ('financial_year', models.IntegerField()),
                ('comment', models.CharField(max_length=255, null=True, blank=True)),
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
        migrations.CreateModel(
            name='Cost',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('cost_date', models.DateField()),
                ('amount', models.FloatField()),
                ('financial_year', models.IntegerField()),
                ('comment', models.CharField(max_length=255, null=True, blank=True)),
            ],
            options={
                'ordering': ['-cost_date'],
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='CostType',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255)),
            ],
            options={
                'ordering': ['name'],
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Game',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('play_date', models.DateField()),
                ('comment', models.CharField(max_length=511, null=True, blank=True)),
            ],
            options={
                'ordering': ['-play_date'],
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='cost',
            name='type',
            field=models.ForeignKey(to='badminton.CostType'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='contribution',
            name='type',
            field=models.ForeignKey(to='badminton.ContributionType'),
            preserve_default=True,
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
        migrations.AddField(
            model_name='contribution',
            name='contributor',
            field=models.ForeignKey(blank=True, to='badminton.Player', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='game',
            name='players',
            field=models.ManyToManyField(to='badminton.Player'),
            preserve_default=True,
        ),
    ]
