from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Listing(models.Model):
    title = models.CharField(max_length=64)
    description = models.CharField(max_length=64)
    starting_bid = models.FloatField()
    category = models.CharField(max_length=64, null=True, blank=True)
    url = models.CharField(max_length=64, null=True, blank=True)
    listed_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="listings")
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} ({self.starting_bid})"

class Bid(models.Model):
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, blank=True, related_name="bid_objects")
    bidder = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, related_name="bids")
    bid = models.FloatField()

    def __str__(self):
        return f"{self.bidder}"

class Comment(models.Model):
    comment = models.CharField(max_length=128)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="comments")
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, blank=True, related_name="comments")

    def __str__(self):
        return f"{self.user}"