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

GRADE_OPTIONS = {
    ('V1', 'V1'),
    ('V2', 'V2'),
    ('V3', 'V3'),
    ('V4', 'V4'),
    ('V5', 'V5'),
    ('V6', 'V6'),
    ('V7', 'V7'),
    ('V8', 'V8'),
    ('V9', 'V9'),
    ('V10', 'V10'),
    ('V11', 'V11'),
    ('V12', 'V12'),
    ('V13', 'V13'),
    ('V14', 'V14'),
    ('V15', 'V15'),
    ('V16', 'V16'),
}

class ClimbLog(models.Model):
    """
    Table for tracking the climb logs of each climber/user
    """
    date = models.DateField()
    grade = models.CharField(max_length=10, choices=GRADE_OPTIONS)
    weather_condition = models.CharField(max_length=50, default="")
    location = models.CharField(max_length=70, default="", null=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    climb_logs = models.Manager()