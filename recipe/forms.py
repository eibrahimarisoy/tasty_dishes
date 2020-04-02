from django import forms
from recipe.models import Rating


class RatingForm(forms.ModelForm):
    class Meta:
        model = Rating
        fields = ['rate', ]
