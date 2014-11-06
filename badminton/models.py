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

    class Meta:
        ordering = ['first_name']
        proxy = True


class CostType(models.Model):
    name = models.CharField(max_length = 255)

    def __unicode__(self):
        return self.name

    class Meta:
        ordering = ['name']


class Cost(models.Model):
    cost_date = models.DateField()
    type = models.ForeignKey(CostType)
    amount = models.FloatField()
    comment = models.CharField(max_length = 255, blank = True, null = True)

    def __unicode__(self):
        return str(self.cost_date)

    class Meta:
        ordering = ['-cost_date']


class Record(models.Model):
    play_date = models.DateField()
    players = models.ManyToManyField(Player)
    comment = models.CharField(max_length = 511, blank = True, null = True)

    def __unicode__(self):
        return str(self.play_date)

    class Meta:
        ordering = ['-play_date']
