# View module for handling requests about game types
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from levelupapi.models import GameType

class GameTypes(ViewSet):

    # Handle GET request for a single game type, return Response -- JSON serialized game type
    def retrieve(self, request, pk=None):
        try:
            game_type = GameType.objects.get(pk=pk)
            serializer = GameTypeSerializer(game_type, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)

    # Handle GET requests to all game types, return Response -- JSON serialized game type
    # Serializer needs many=True argument on multiples
    def list(self, request):
        gametypes = GameType.objects.all()

        serializer = GameTypeSerializer(gametypes, many=True, context={'request': request})
        return Response(serializer.data)
        
# Serializer

class GameTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = GameType
        fields = ('id', 'label')