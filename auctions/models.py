from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    watchlist = models.ManyToManyField("Listing")
    pass

class Listing(models.Model):
    title = models.CharField(max_length= 100)
    description = models.TextField()
    imageURL = models.URLField(blank=True)
    initBid = models.DecimalField(max_digits= 10, decimal_places= 2)
    
    category = models.ManyToManyField("Category", null= True, blank=True)

    createTime = models.DateTimeField(auto_now_add= True)
    changeTime = models.DateTimeField(auto_now= True)

    createUser = models.ForeignKey(User, on_delete= models.CASCADE)

    closed = models.BooleanField(null= True, default= False)

class Bid(models.Model):
    value = models.DecimalField(max_digits= 10, decimal_places= 2)
    user = models.ForeignKey(User, on_delete= models.CASCADE)
    createTime = models.DateTimeField(auto_now_add= True)
    listing = models.ForeignKey(Listing, on_delete= models.CASCADE)

class Category(models.Model):
    type = models.CharField(max_length= 50)

class Comment(models.Model):
    listing = models.ForeignKey(Listing, on_delete= models.CASCADE)
    user = models.ForeignKey(User, on_delete= models.CASCADE)
    comment = models.TextField()
    createTime = models.DateTimeField(auto_now_add= True)