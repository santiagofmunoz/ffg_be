import io
from PIL import Image
from django.http import FileResponse
from reportlab.lib.units import mm
from reportlab.pdfgen import canvas
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .serializers import *


def position_switcher(position_name):
    switcher = {
        "Golero": [250, 750],
        "Carrilero izquierdo": [430, 580],
        "Carrilero derecho": [100, 580],
        "Lateral izquierdo": [430, 650],
        "Lateral derecho": [100, 650],
        "Central izquierdo": [330, 650],
        "Central derecho": [190, 650],
        "Central": [250, 680],
        "Mediocampista defensivo": [250, 500],
        "Interior izquierdo": [430, 430],
        "Interior derecho": [100, 430],
        "Mediocentro izquierdo": [330, 430],
        "Mediocentro derecho": [180, 430],
        "Media punta": [250, 340],
        "Delantero central": [250, 200],
        "Volante izquierdo": [350, 250],
        "Volante derecho": [170, 250],
        "Extremo izquierdo": [430, 250],
        "Extremo derecho": [100, 250],
    }
    return switcher.get(position_name, [0, 1])


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


@api_view(['GET'])
def get_formations(request):
    formations = Formation.objects.all()
    serializer = FormationSerializer(formations, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def export_formation_as_pdf(request, formation_id):
    # Se crea un buffer para crear la información del PDF
    buffer = io.BytesIO()
    # Se crea el PDF, utilizando el buffer y su archivo.
    p = canvas.Canvas(buffer)
    # Se dibuja la cancha de fútbol
    cancha_futbol = Image.open("res/img/cancha_futbol.jpeg")
    p.drawInlineImage(cancha_futbol, 26 * mm, 24 * mm)

    formation_players = PlayerFormation.objects.all().filter(formation_id=formation_id)
    serialized_formation_players = PlayerFormationSerializer(formation_players, many=True)
    for player in serialized_formation_players.data:
        player_id = player['player']
        get_player = Player.objects.get(player_id=player_id)
        serialized_get_player = PlayerSerializer(get_player)
        player_obj = serialized_get_player.data
        player_position_id = player_obj['position']
        get_position = Position.objects.get(position_id=player_position_id)
        serialized_get_position = PositionSerializer(get_position)
        position_obj = serialized_get_position.data
        position_name = position_obj['position_name']
        xy_values = position_switcher(position_name)
        player_name = player_obj['player_first_name'] + " " + player_obj['player_last_name']
        p.drawString(xy_values[0], xy_values[1], player_name)

    # Se cierra el PDF
    p.showPage()
    p.save()

    # Se retorna el PDF al cliente
    buffer.seek(0)
    return FileResponse(buffer, as_attachment=False, filename='formacion.pdf')
