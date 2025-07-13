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

    def __init__(self, *args, listing = None, **kwatgsd
                 ):
        super().__init__(data, files, auto_id, prefix, initial, error_class, label_suffix, empty_permitted, instance, use_required_attribute, renderer)
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