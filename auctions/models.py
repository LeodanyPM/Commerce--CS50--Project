from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass
    
class Listing(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_ads")
    title = models.CharField(max_length=60)
    category = models.CharField(max_length=60, null=True)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)  
    date = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to='ads_images/', blank=True, null=True)  
    
    
    class Meta:
        ordering = ['-date']  
        
    def __str__(self):
        return self.title
        
"""class Comment(models.Model):
     user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_ads")
     comment = models.TextField()
     date = models.DateTimeField(auto_now_add=True)
     
     class Meta:
        ordering = ['-date']"""
      
