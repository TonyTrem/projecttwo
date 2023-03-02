from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Listing(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=128)
    description = models.TextField()
    current_bid = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    starting_bid = models.DecimalField(max_digits=10, decimal_places=2, blank=True)
    creation_date = models.DateTimeField(auto_now_add=True)
    image_url = models.CharField(max_length=64)
    category = models.CharField(max_length=128, blank=True)
    active = models.BooleanField(default=True)
    bid_count = models.IntegerField(default=1)
    expiration_date = models.DateTimeField(blank=True, null=True)
    
    def __str__(self):
        return f"{self.title} {self.description} {self.starting_bid} {self.image_url} {self.category} {self.active} {self.user}"
    
class Bid(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE)
    bid = models.DecimalField(max_digits=10, decimal_places=2)
    bid_date = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.user} {self.listing} {self.bid} {self.bid_date}"