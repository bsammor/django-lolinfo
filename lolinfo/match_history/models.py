from django.db import models
from django.conf import settings
from django.db.models import JSONField

class Summoner(models.Model):
    class Meta:
        unique_together = (('name', 'region'),)

    name = models.TextField(primary_key=True, max_length=100)
    region = models.CharField(max_length=9, choices=[(0, 'EUW'), (1, 'NA'), (2, 'EUNE')], default=0)
    icon_id = models.IntegerField(default=0)
    level = models.IntegerField(default=0)
    lp = models.IntegerField(null=True)
    rank = models.TextField(max_length=50, null=True)
    tier = models.CharField(max_length=50, null=True)
    winrate = models.FloatField(null=True)
    wins = models.IntegerField(null=True)
    losses = models.IntegerField(null=True)
    matches_ref = JSONField(null=True)
    matches_history = JSONField(null=True)