from django.db import models

# Create your models here.
class User(models.Model):
    """
    Keep track of the different users who log in to track their climbs
    """
    username = models.CharField(max_length=50, default="", blank=True, null=False)
    password = models.CharField(max_length=50, default="", null=False)

    users = models.Manager()

    def __str__(self):
        return self.username

class ClimbLog(models.Model):
    """
    Table for tracking the climb logs of each climber/user
    """
    date = models.DateField()
    grade = models.CharField(max_length=10)
    weather_condition = models.CharField(max_length=50, default="")
    location = models.CharField(max_length=70, default="", null=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    climb_logs = models.Manager()