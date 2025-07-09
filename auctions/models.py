from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    watchlist = models.ForeignKey("Listing", on_delete=models.CASCADE)

class Listing(models.Model):
    title = models.CharField(max_length= 100)
    description = models.TextField()
    imageURL = models.URLField()
    initBid = models.DecimalField(max_digits= 10, decimal_places= 2)
    
    category = models.ManyToManyField("Category")

    biggerBid = models.ForeignKey("Bid", on_delete= models.SET_NULL, null= True, blank= True)

    createTime = models.DateTimeField(auto_now_add= True)
    changeTime = models.DateTimeField(auto_now= True)

    createUser = models.ForeignKey(User, on_delete= models.CASCADE)

    closed = models.BooleanField(null= True, default= False)

   
