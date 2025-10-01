from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models import Max


class User(AbstractUser):
    pass

class Category(models.Model):
    name = models.CharField(max_length=300)
    class Meta:
        ordering = ['name']
    def __str__(self):
        return self.name
    
class Listing(models.Model):
    title = models.CharField(max_length=200)
    description = models.CharField(max_length=300)
    start_bid = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.URLField(max_length=100, blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    active = models.BooleanField(default=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="listings")
    created_at = models.DateTimeField(auto_now_add=True)
    watchlisted_by = models.ManyToManyField(User, related_name="watchlist", blank=True)

    def __str__(self):
        return self.title
    
    def no_of_bids(self):
        return self.bids.all().count()
    def current_price(self):
        if self.no_of_bids() > 0:
            return round(self.bids.aggregate(Max("amount"))["amount__max"])
        else:
            return self.start_bid
    def is_in_watchlist(self, user):
        return user.watchlist.filter(pk=self.pk).exists()
    
    class Meta:
        ordering = ['-created_at']
    
class Bid(models.Model):
    item = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="bids")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bids")
    amount = models.DecimalField(max_digits=6, decimal_places=2)

    def __str__(self):
        return str(self.amount)
class Comment(models.Model):
    item = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="comments")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments")
    comment = models.CharField(max_length=1000)
    time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.comment)

    class Meta:
        ordering = ['-time']