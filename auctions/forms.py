from django.forms import ModelForm
from django.core.exceptions import ValidationError

from .models import Listing, Category, Bid, Comment

from decimal import Decimal

from .utils import getCurrentBidValue

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
    def __init__(self, *args, listing, **kwargs):
        super().__init__(*args, **kwargs)
        self.listing = listing
        self.currentValue, currentBid = getCurrentBidValue(listing)
        self.fields["value"].initial = self.currentValue + Decimal("0.01")
    class Meta:
        model = Bid
        fields = [
            "value"
        ]

    
class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = [
            "comment"
        ]


