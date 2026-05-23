from django.contrib.auth.models import AbstractUser
from django.db import models
from .util import optimize_image
from django.core.files.uploadedfile import InMemoryUploadedFile
from io import BytesIO 


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
    active = models.BooleanField(default=True)
    winner = models.ForeignKey(User,null=True, blank=True, on_delete=models.CASCADE, related_name="winner") 
    
    
    class Meta:
        ordering = ['-date']
    
    def save(self, *args, **kwargs):
        if self.image and hasattr(self.image, 'file'):
            try:
                optimized = optimize_image(
                    self.image.file,
                    max_size=(1200, 1200),
                    quality=85
                )
                self.image = optimized
            except Exception as e:
                print(f"⚠️ Error optimizando: {e}")
        
        super().save(*args, **kwargs)
            
    def __str__(self):
        return self.title
        
"""class Comment(models.Model):
     user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_ads")
     comment = models.TextField()
     date = models.DateTimeField(auto_now_add=True)
     
     class Meta:
        ordering = ['-date']"""
class Watchlist(models.Model):
      user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="watchlist")
      listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="watched_by")
      date = models.DateTimeField(auto_now_add=True)
      class Meta:
          constraints = [models.UniqueConstraint(fields=['user', 'listing'], name='unique_user_listing')]
          indexes = [models.Index(fields=['user',])]
      def __str__(self):
      	 return  f"{self.user.username} : {self.listing.title}"    
