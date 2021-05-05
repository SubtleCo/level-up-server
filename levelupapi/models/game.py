from django.db import models

class Game(models.Model):
    title = models.CharField(max_length=50, null=True)
    maker = models.CharField(max_length=50, null=True)
    gamer = models.ForeignKey("Gamer", on_delete=models.DO_NOTHING)
    gametype = models.ForeignKey("GameType", on_delete=models.CASCADE)
    skill_level = models.IntegerField(default=0)
    number_of_players = models.IntegerField(null=True)