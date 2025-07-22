from django.forms import ModelForm
from .models import User, ClimbLog

class UserForm(ModelForm):
    class Meta:
        model = User
        fields = '__all__'

class ClimbLogForm(ModelForm):
    class Meta:
        model = ClimbLog
        fields = '__all__'