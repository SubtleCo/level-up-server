from django.db import models

class Event(models.Model):
    date = models.DateField(null=True)
    time = models.TimeField(null=True)
    game = models.ForeignKey("Game", on_delete=models.CASCADE, null=True, related_name='events')
    description = models.CharField(max_length=100, null=True)
    organizer = models.ForeignKey("Gamer", on_delete=models.CASCADE, null=True, related_name="organizer")
    attendees = models.ManyToManyField("Gamer", through="EventGamer", related_name="attending")

    @property
    def joined(self):
        return self.__joined

# Since the Q filter is using a COUNT, the result will be 1 or 0. Make it a bool.
    @joined.setter
    def joined(self, value):
        self.__joined = bool(value)

    @property
    def attendee_count(self):
        return self.__attendee_count

    @attendee_count.setter
    def attendee_count(self, value):
        self.__attendee_count = value



    

