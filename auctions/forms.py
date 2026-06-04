from django import forms
from .models import Listing, Comment, Bid
#, Comment

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
        
class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['comment']
        labels = {'comment': 'Comment' }
        widgets = {
              'comment': forms.Textarea(attrs={
               'rows': 3, 
               'class': 'form-control', 
               'placeholder': 'Escribe tu opinión aquí...'
            })
        }
        
class BidForm(forms.Form):
    bid_amount = forms.DecimalField(
        max_digits=10,
        decimal_places=2,
        min_value=0.01,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'Monto de tu puja',
            'step': '0.01',
            'required': True
        })
    ) 
