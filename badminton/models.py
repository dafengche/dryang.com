from django.contrib.auth.models import User
from django.db import models
"""
# I want to add new attributes/functions to User
class Player(models.Model):
    user = models.OneToOneField(User)

    def __unicode__(self):
        return self.user.first_name + ' ' + self.user.last_name
"""


# Player is a proxy model of User as no extension involved
class Player(User):
    def __unicode__(self):
        return self.first_name + ' ' + self.last_name

    def as_json(self):
        return dict(
            username = self.username,
            first_name = self.first_name,
            last_name = self.last_name)


    class Meta:
        ordering = ['first_name']
        proxy = True


class CostType(models.Model):
    name = models.CharField(max_length = 255)

    def __unicode__(self):
        return self.name

    def as_json(self):
        return dict(name = self.name)


    class Meta:
        ordering = ['name']


class Cost(models.Model):
    cost_date = models.DateField()
    type = models.ForeignKey(CostType)
    amount = models.FloatField()
    financial_year = models.IntegerField()
    comment = models.CharField(max_length = 255, blank = True, null = True)

    def __unicode__(self):
        return str(self.cost_date)

    def as_json(self):
        return dict(
            date = self.cost_date.isoformat(),
            type = self.type.as_json(),
            amount = self.amount,
            financial_year = self.financial_year,
            comment = self.comment)


    class Meta:
        ordering = ['-cost_date']


class Game(models.Model):
    play_date = models.DateField()
    players = models.ManyToManyField(Player)
    comment = models.CharField(max_length = 511, blank = True, null = True)

    def __unicode__(self):
        return str(self.play_date)

    def as_json(self):
        return dict(
            date = self.play_date.isoformat(),
            players = [p.as_json() for p in self.players.all()],
            comment = self.comment)


    class Meta:
        ordering = ['-play_date']


class ContributionType(models.Model):
    name = models.CharField(max_length = 255)

    def __unicode__(self):
        return self.name

    def as_json(self):
        return dict(name = self.name)


    class Meta:
        ordering = ['name']


class Contribution(models.Model):
    contribution_date = models.DateField()
    type = models.ForeignKey(ContributionType)
    amount = models.FloatField()
    financial_year = models.IntegerField()
    contributor = models.ForeignKey(Player, blank = True, null = True)
    comment = models.CharField(max_length = 255, blank = True, null = True)

    def __unicode__(self):
        return str(self.contribution_date)

    def as_json(self):
        d = dict(
            date = self.contribution_date.isoformat(),
            type = self.type.as_json(),
            amount = self.amount,
            financial_year = self.financial_year,
            contributor = '',
            comment = self.comment)
        if self.contributor:
           d.update(contributor = self.contributor.as_json())
        return d

    class Meta:
        ordering = ['-contribution_date']
