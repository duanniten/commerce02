from django.forms import ModelForm

from .models import Listing, Category, Bid

class CreateListingForm(ModelForm):
    class Meta:
        models = Listing
        fields = [
            "title",
            "description",
            "imageURL",
            "initBid",
            "category"            
        ]
class CreateCategory(ModelForm):
    class Meta:
        models = Category
        fields = [
            'type'
        ]

class MakeBid(ModelForm):
    class Meta:
        models = Bid
        fields = [
            "value"
        ]

class CloseListing(ModelForm):
    class Meta:
        models = Listing
        fields = [
            "closed"
        ]