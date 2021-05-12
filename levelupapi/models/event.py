from django.db import models

class Event(models.Model):
    date = models.DateField(null=True)
    time = models.TimeField(null=True)
    game = models.ForeignKey("Game", on_delete=models.CASCADE, null=True, related_name='events')
    description = models.CharField(max_length=100, null=True)
    organizer = models.ForeignKey("Gamer", on_delete=models.CASCADE, null=True)
    attendees = models.ManyToManyField("Gamer", through="EventGamer", related_name="attending")

    @property
    def joined(self):
        return self.__joined

    @joined.setter
    def joined(self, value):
        self.__joined = value

