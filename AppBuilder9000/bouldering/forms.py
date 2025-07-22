from django.forms import ModelForm
from .models import User, ClimbLog

class UserForm(ModelForm):
    class Meta:
        model = User
        fields = '__all__'

class ClimbLogForm(ModelForm):
    class Meta:
        model = ClimbLog
        # not allowing user to enter 'user' entry for when the user submits the form
        # they entry will be filled in the views.py
        fields = ('date', 'grade', 'weather_condition', 'location')