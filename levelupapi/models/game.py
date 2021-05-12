from django.db import models

class Game(models.Model):
    title = models.CharField(max_length=50, null=True)
    maker = models.CharField(max_length=50, null=True)
    gamer = models.ForeignKey("Gamer", on_delete=models.DO_NOTHING)
    gametype = models.ForeignKey("GameType", on_delete=models.CASCADE)
    skill_level = models.IntegerField(default=0)
    number_of_players = models.IntegerField(null=True)

    @property
    def event_count(self):
        return self.__event_count

    @event_count.setter
    def event_count(self, value):
        self.__event_count = value

    @property
    def user_event_count(self):
        return self.__user_event_count

    @user_event_count.setter
    def user_event_count(self, value):
        self.__user_event_count = value