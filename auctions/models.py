from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    watchlist = models.ForeignKey("Listing", on_delete=models.CASCADE)

