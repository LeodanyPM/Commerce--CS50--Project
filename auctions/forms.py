from django import forms
from .models import Listing

class ListingForm(forms.ModelForm):
    class Meta:
        model = Listing
        fields = ['title','category', 'price',  'description', 'image']
        labels = {
            'title': 'Títle:',
            'category': 'Category:',
            'price': 'Price:',
            'description' : 'Description:',
            'image': 'Upload image:' 
        }
        widgets = {
            'description': forms.Textarea(attrs={'rows': 6, 'class': 'form-control'}),
        }
        # fields = '__all__'  # o excluir: exclude = ['creado_en']
