from django.db import models


class Position(models.Model):
    name = models.CharField("Name", max_length=255, unique=True)


class Player(models.Model):
    name = models.CharField("Name", max_length=255)
    position = models.ForeignKey(Position, models.CASCADE)

    def get_pk(self):
        return self.pk


class Formation(models.Model):
    name = models.CharField("Name", max_length=255)
    num_def = models.IntegerField("Number_Defenders")
    num_mid = models.IntegerField("Number_Midfielders")
    num_fwd = models.IntegerField("Number_Forwards")


class PlayerFormation(models.Model):
    player = models.ForeignKey(Player, models.CASCADE)
    formation = models.ForeignKey(Formation, models.CASCADE)
