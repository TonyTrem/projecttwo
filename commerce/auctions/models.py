from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Listing(models.Model):
    user = models.CharField(max_length=64)
    title = models.CharField(max_length=128)
    description = models.TextField()
    starting_bid = models.DecimalField(max_digits=10, decimal_places=2, blank=True)
    creation_date = models.DateTimeField(auto_now_add=True)
    image_url = models.CharField(max_length=256, default = None, blank = True, null = True)
    category = models.CharField(max_length=128, blank=True)
    active = models.BooleanField(default=True)
   
    def __str__(self):
        return f"{self.title} {self.user} {self.creation_date} {self.active}"
    
     
class Bid(models.Model):
    user = models.CharField(max_length=64)
    listingid = models.IntegerField()
    bid = models.DecimalField(max_digits=10, decimal_places=2)
    
    def __str__(self):
        return f"{self.user} {self.listingid} {self.bid}"
    

class Comment(models.Model):
    user = models.CharField(max_length=64)
    listingid = models.IntegerField()
    comment = models.TextField()
   
    def __str__(self):
        return f"{self.user} {self.listingid} {self.comment}"


class Watchlist(models.Model):    
    watch_list = models.ForeignKey(Listing, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.watch_list} {self.user}"
    