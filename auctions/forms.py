from django import forms
from .models import Listing, Comment



class ListingForm(forms.ModelForm):
    class Meta:
        model = Listing
        fields = ['title', 'category', 'price', 'description', 'image']
        labels = {
            'title': 'Title',
            'category': 'Category',
            'price': 'Starting Price',
            'description': 'Description',
            'image': 'Upload Image'
        }
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
            'price': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'image': forms.FileInput(attrs={'class': 'form-control-file'}),
        }
        
        error_messages = {
            'title': {'required': 'The title is required.'},
            'category': {'required': 'Select a category.'},
            'price': {'required': 'Enter a starting price.'},
            'description': {'required': 'The description cannot be empty.'},
        }
        


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['comment']
        labels = {'comment': 'Comment' }
        widgets = {
              'comment': forms.Textarea(attrs={
               'rows': 3, 
               'class': 'form-control', 
               'placeholder': 'Write your opinion here...'
            })
        }
        

