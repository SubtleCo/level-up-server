from django.db import models

class Game(models.Model):
    game_type_id = models.ForeignKey("GameType", on_delete=models.CASCADE)
    players = models.IntegerField(null=True)
    name = models.CharField(max_length=50, null=True)