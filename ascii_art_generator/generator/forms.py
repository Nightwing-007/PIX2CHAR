from django import forms
from .models import AsciiArt

class AsciiArtForm(forms.ModelForm):
    """Form for ASCII art generation"""
    title = forms.CharField(max_length=100, required=False, 
                          widget=forms.TextInput(attrs={'class': 'form-control'}))
    width = forms.IntegerField(min_value=20, max_value=300, initial=100,
                             widget=forms.NumberInput(attrs={'class': 'form-control'}))
    
    class Meta:
        model = AsciiArt
        fields = ['title', 'original_image', 'width']
        widgets = {
            'original_image': forms.FileInput(attrs={'class': 'form-control'})
        }