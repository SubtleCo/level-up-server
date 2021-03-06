### View module for handling requests about games

from django.core.exceptions import ValidationError
from rest_framework import status
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from levelupapi.models import Game, GameType, Gamer
from django.db.models import Count, Q

class Games(ViewSet):

    ################################  CREATE  ################################
  
    def create(self, request):

        # Use token to identify user
        gamer = Gamer.objects.get(user=request.auth.user)

        # Create an instance of a game and use request body data to fill it in
        game = Game()
        game.title = request.data["title"]
        game.maker = request.data["maker"]
        game.number_of_players = request.data["numberOfPlayers"]
        game.skill_level = request.data["skillLevel"]
        game.gamer = gamer

        # use Django ORM to get record from DB whose 'id' is what the client passed as 'gameTypeId' in body
        gametype = GameType.objects.get(pk=request.data["gameTypeId"])
        game.gametype = gametype

        # Try to save new game to DB, then serialize it to JSON and send it back
        try:
            game.save()
            serializer = GameSerializer(game, context={'request': request})
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        # If anything went wrong, catch the exception and send a 400 code
        except ValidationError as ex:
            return Response({"reason": ex.message}, status=status.HTTP_400_BAD_REQUEST)


    ################################  RETRIEVE  ################################

    def retrieve(self, request, pk=None):
        try:
            game = Game.objects.get(pk=pk)
            serializer = GameSerializer(game, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex, status=status.HTTP_404_NOT_FOUND)

    ################################  UPDATE  ################################

    def update(self, request, pk=None):
        gamer = Gamer.objects.get(user = request.auth.user)
        game = Game.objects.get(pk=pk)
        game.title = request.data["title"]
        game.maker = request.data["maker"]
        game.number_of_players = request.data["numberOfPlayers"]
        game.skill_level = request.data["skillLevel"]
        game.gamer = gamer

        gametype = GameType.objects.get(pk=request.data["gameTypeId"])
        game.gametype = gametype
        game.save()

        # 204 means everything worked, but you won't get a response
        return Response({}, status=status.HTTP_204_NO_CONTENT)

    ################################  DESTROY  ################################

    def destroy(self, request, pk=None):
        try:
            game = Game.objects.get(pk=pk)
            game.delete()

            return Response({}, status=status.HTTP_204_NO_CONTENT)

        except Game.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)
        
        except Exception as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    ################################  LIST  ################################

    def list(self, request):

        gamer = Gamer.objects.get(user=request.auth.user)
        # Get all the game records from the DB
        games = Game.objects.annotate(
            event_count=Count('events'),
            user_event_count=Count(
                'events',
                # In this case, the dunder is expanding the object: {Game} --> [events] >>> {event} --> {organizer}
                filter=Q(events__organizer=gamer)
                )
            )
        # for game in games:
        #     game.user_event_count = 0
        #     for event in game.events.all():
        #         if (event.organizer == gamer): game.user_event_count += 1

        # Support filtering games by type
        game_type = self.request.query_params.get('type', None)
        if game_type is not None:
            # the double underscore __ denotes "join gametype on id"
            games = games.filter(gametype__id=game_type)

        serializer = GameSerializer(
            games, many=True, context={'request': request})
        return Response(serializer.data)



################################  SERIALIZER  ################################

class GameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Game
        fields = ('id', 'title', 'maker', 'number_of_players', 'skill_level', 'gametype', 'event_count', 'user_event_count')
        depth = 1

