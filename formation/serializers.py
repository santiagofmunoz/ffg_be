from rest_framework import serializers
from .models import *


class PositionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Position
        fields = ('pk', 'position_name', 'type')


class PlayerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Player
        fields = ('pk', 'player_first_name', 'player_last_name', 'position')


class FormationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Formation
        fields = ('pk', 'formation_name', 'num_def', 'num_mid', 'num_fwd')


class PlayerFormationSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlayerFormation
        fields = ('pk', 'player', 'formation')
