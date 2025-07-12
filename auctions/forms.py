from django.forms import ModelForm

from .models import Listing, Category, Bid

class CreateListingForm(ModelForm):
    class Meta:
        model = Listing
        fields = [
            "title",
            "description",
            "imageURL",
            "initBid",
            "category"            
        ]
class CreateCategory(ModelForm):
    class Meta:
        model = Category
        fields = [
            'type'
        ]

class MakeBid(ModelForm):
    class Meta:
        model = Bid
        fields = [
            "value"
        ]

class CloseListing(ModelForm):
    class Meta:
        model = Listing
        fields = [
            "closed"
        ]