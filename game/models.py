from django.db import models
# Create your models here.



class Hero(models.Model):
    name = models.CharField(max_length=255)
    describe = models.CharField(max_length=255)
    power = models.IntegerField()

    def __str__(self):
        return self.name
    

class Map(models.Model):
    name = models.CharField(max_length=255, unique=True)
    describe = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class Team(models.Model):
    name = models.CharField(max_length=255, unique=True)
    user = models.ForeignKey('user.User', on_delete=models.CASCADE, related_name='teams')
    amount = models.IntegerField(null=True, blank=True)
    total_power = models.IntegerField(null=True, blank=True)
    heroes = models.ManyToManyField(Hero, through='HeroTeam')

    def __str__(self):
        return self.name


class HeroTeam(models.Model):
    team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='hero_team')
    hero = models.ForeignKey(Hero, on_delete=models.CASCADE, related_name='hero_team')
    is_captain = models.BooleanField(default=False)

    def __str__(self):
        return str(self.team)