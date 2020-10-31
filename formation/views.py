from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .serializers import *


@api_view(['POST'])
def create_player(request):
    serializer = PlayerSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def create_formation(request):
    players_obj = request.data['players']
    serializer = FormationSerializer(data=request.data)
    if serializer.is_valid():
        created_formation = serializer.save()
        formation_id = created_formation.get_pk()
        get_created_formation = Formation.objects.get(formation_id=formation_id)
        for key in players_obj:
            player_id = players_obj[key]
            get_player = Player.objects.get(player_id=player_id)
            PlayerFormation.objects.create(formation=get_created_formation, player=get_player)

    return Response(status=status.HTTP_200_OK);


@api_view(['GET'])
def get_players_position_detail(request):
    try:
        players = Player.objects.all()
    except Player.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    serializer = PlayerPositionSerializer(players, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def get_positions(request):
    positions = Position.objects.all()
    serializer = PositionSerializer(positions, many=True)
    return Response(serializer.data)
