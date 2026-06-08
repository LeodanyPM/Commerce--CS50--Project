from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.files.uploadedfile import InMemoryUploadedFile
from io import BytesIO 


class User(AbstractUser):
    pass

class Category(models.Model):
    category = models.CharField(max_length=60, unique=True)
    class Meta:
        ordering = ['category']
    
    def __str__(self):
       return f"{self.category}"
    
class Listing(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_ads")
    title = models.CharField(max_length=60)
    category = models.ForeignKey(Category, on_delete= models.PROTECT, related_name="listing")
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)  
    date = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to='ads_images/', blank=True, null=True)
    active = models.BooleanField(default=True)
    winner = models.ForeignKey(User,null=True, blank=True, on_delete=models.SET_NULL, related_name="winner") 
    
    
    class Meta:
        ordering = ['-date']


                
    def __str__(self):
        return self.title
    
 
class Bid(models.Model):
    user = models.ForeignKey(User,null=True, blank=True, on_delete=models.SET_NULL, related_name="bids")
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="bids")
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-amount'] 
        

    def __str__(self):
        return f"{self.user.username if self.user else 'Unknown'} : ${self.amount}"
        
        
class Comment(models.Model):
     listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name='comments')
     user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_comment")
     comment = models.TextField()
     date = models.DateTimeField(auto_now_add=True)
     
     class Meta:
        ordering = ['-date']     
         

     def __str__(self):
        return f"{self.user.username} in {self.listing.title}"
class Watchlist(models.Model):
      user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="watchlist")
      listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="watched_by")
      date = models.DateTimeField(auto_now_add=True)
      class Meta:
          constraints = [models.UniqueConstraint(fields=['user', 'listing'], name='unique_user_listing')]
          
      def __str__(self):
      	 return  f"{self.user.username} : {self.listing.title}"    
