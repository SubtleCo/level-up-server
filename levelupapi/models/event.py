from django.db import models

class Event(models.Model):
    date = models.DateTimeField()
    location = models.CharField(max_length=50)
    game = models.ForeignKey("Game", on_delete=models.CASCADE, null=True)
    host = models.ForeignKey("Gamer", on_delete=models.CASCADE, null=True)

