from django import forms
from .models import UserProfile

class ProfilePictureForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['profile_picture']


class SimulationForm(forms.Form):
    animal_type = forms.ChoiceField(choices=[('herbivore', 'Herbivore'), ('carnivore', 'Carnivore')])
    simulation_speed = forms.IntegerField(min_value=1, max_value=10, label='Simulation Speed')