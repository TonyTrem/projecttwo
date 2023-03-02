from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Listing(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=64)
    description = models.CharField(max_length=64)
    starting_bid = models.IntegerField()
    current_bid = models.IntegerField()
    creation_date = models.DateTimeField(auto_now_add=True)
    image_url = models.CharField(max_length=64)
    category = models.CharField(max_length=64)
    active = models.BooleanField(default=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="listings")

    def __str__(self):
        return f"{self.title} {self.description} {self.starting_bid} {self.image_url} {self.category} {self.active} {self.user}"