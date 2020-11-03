import io
from PIL import Image
from django.http import FileResponse
from reportlab.lib.units import mm
from reportlab.pdfgen import canvas
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .serializers import *


# Implementation of SWITCH-CASE to return information based on the position_name given.
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


# Player creation. Receives a player object as a parameter. Checks if the information provided is correct and after
# that, persists the object
@api_view(['POST'])
def create_player(request):
    serializer = PlayerSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Formation creation. Receives a formation object as a parameter.
@api_view(['POST'])
def create_formation(request):
    # We get the players' infromation from the request.data object
    players_obj = request.data['players']
    # Formation data is serialized in FormationSerializer
    serializer = FormationSerializer(data=request.data)
    # We check if the information provided is valid.
    if serializer.is_valid():
        # We save the formation information in the database and we grab the created object.
        created_formation = serializer.save()
        # Now we iterate in players_obj to get each player in the formation.
        for key in players_obj:
            # We get the player_id
            player_id = players_obj[key]
            # We search for the player object stored in the database
            get_player = Player.objects.get(player_id=player_id)
            # We create the association between the formation and the player.
            PlayerFormation.objects.create(formation=created_formation, player=get_player)
            # This piece of code repeats until all players are associated with the formation
        return Response(status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Returns all the players in the system with the information of each one's position. If there aren't any players, a 404
# status is returned. Otherwise, the list of players is returned.
@api_view(['GET'])
def get_players_position_detail(request):
    try:
        players = Player.objects.all()
    except Player.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    serializer = PlayerPositionSerializer(players, many=True)
    return Response(serializer.data)


# Returns all the positions
@api_view(['GET'])
def get_positions(request):
    positions = Position.objects.all()
    serializer = PositionSerializer(positions, many=True)
    return Response(serializer.data)


# Returns all the formations
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

    # We get the information of Player-Formation filtered by the id of the desired formation.
    formation_players = PlayerFormation.objects.all().filter(formation_id=formation_id)
    # We serialise the data of Player-Formation to check it's integrity.
    serialized_formation_players = PlayerFormationSerializer(formation_players, many=True)
    # For every player that's in the formation...
    for player in serialized_formation_players.data:
        # We get the player's id.
        player_id = player['player']
        # We get the player's object filtered by it's id
        get_player = Player.objects.get(player_id=player_id)
        # We serialise the object to check it's integrity
        serialized_get_player = PlayerSerializer(get_player)
        # We get the player object
        player_obj = serialized_get_player.data
        # We get the position id from the player's object
        player_position_id = player_obj['position']
        # We get the position object
        get_position = Position.objects.get(position_id=player_position_id)
        # We serialise the object to check it's integrity.
        serialized_get_position = PositionSerializer(get_position)
        # We get the position object.
        position_obj = serialized_get_position.data
        # We get the position name from the object
        position_name = position_obj['position_name']
        # We send the position name to the SWITCH-CASE function and the function will return us the (x, y) values for
        # the PDF
        xy_values = position_switcher(position_name)
        # We get the player's full name to print it in the PDF.
        player_name = player_obj['player_first_name'] + " " + player_obj['player_last_name']
        # We draw the string of the player's full name in the provided (x, y) values.
        p.drawString(xy_values[0], xy_values[1], player_name)
        # This piece of code repeats for each player in the formation.

    # Se cierra el PDF
    p.showPage()
    p.save()

    # Se retorna el PDF al cliente
    buffer.seek(0)
    return FileResponse(buffer, as_attachment=False, filename='formacion.pdf')
