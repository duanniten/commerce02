from django.contrib import admin

from .models import Bid, Listing, User, Category

admin.site.register(Bid)
admin.site.register(Listing)
admin.site.register(User)
admin.site.register(Category)
