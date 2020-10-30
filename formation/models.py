from django.db import models


class Position(models.Model):
    class PositionTypes(models.TextChoices):
        GOL = "Golero"
        DEF = "Defensa"
        MED = "Mediocampista"
        DEL = "Delantero"
        DIR = "Director Tecnico"

    position_id = models.AutoField(primary_key=True)
    position_name = models.CharField("position_name", max_length=255)
    type = models.CharField(max_length=16, choices=PositionTypes.choices)


class Player(models.Model):
    player_id = models.AutoField(primary_key=True)
    player_first_name = models.CharField("player_first_name", max_length=255)
    player_last_name = models.CharField("player_last_name", max_length=255)
    position = models.ForeignKey(Position, models.CASCADE, related_name="player_position")

    def get_pk(self):
        return self.player_id


class Formation(models.Model):
    formation_id = models.AutoField(primary_key=True)
    formation_name = models.CharField("formation_name", max_length=255)
    num_def = models.IntegerField("number_defenders")
    num_mid = models.IntegerField("number_midfielders")
    num_fwd = models.IntegerField("number_forwards")


class PlayerFormation(models.Model):
    player_formation_id = models.AutoField(primary_key=True)
    player = models.ForeignKey(Player, models.CASCADE)
    formation = models.ForeignKey(Formation, models.CASCADE)
