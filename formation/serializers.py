from rest_framework import serializers
from .models import *


class PositionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Position
        fields = ('position_id', 'position_name', 'type')


class PlayerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Player
        fields = ('player_id', 'player_first_name', 'player_last_name', 'position')


# This serializer was created to support the situation where you need to do a JOIN with Position table and get the
# information from Position table as well
class PlayerPositionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Player
        depth = 1
        fields = ('player_id', 'player_first_name', 'player_last_name', 'position')


class FormationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Formation
        fields = ('formation_id', 'formation_name', 'num_def', 'num_mid', 'num_fwd')


class PlayerFormationSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlayerFormation
        fields = ('player_formation_id', 'player', 'formation')
