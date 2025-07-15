from django.forms import ModelForm
from django.core.exceptions import ValidationError

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
    def __init__(self, *args, listing :Listing, **kwatgsd):
        super().__init__(*args, **kwatgsd)
        self.listing = listing

    class Meta:
        model = Bid
        fields = [
            "value"
        ]
    
    def clean_value(self):
        value = self.cleaned_data["value"]
        biger_bid  = Bid.objects.filter(listing = self.listing).order_by('-value').first()
        if value <= biger_bid.value:
            raise ValidationError(f"Bid should be biger than atual bid, ${biger_bid:.2f}")
        return value

class CloseListing(ModelForm):
    class Meta:
        model = Listing
        fields = [
            "closed"
        ]