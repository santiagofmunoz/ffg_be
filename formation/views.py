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


@api_view(['GET'])
def get_position_by_type(request, typ):
    try:
        position = Position.objects.filter(type=typ)
    except Position.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    serializer = PositionSerializer(position, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def get_positions(request):
    positions = Position.objects.all()
    serializer = PositionSerializer(positions, many=True)
    return Response(serializer.data)
