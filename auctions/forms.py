from django.forms import ModelForm

from .models import Listing

class CreateListingForm(ModelForm):
    class Meta:
        models = Listing
        fields = [
            "title",
            "description",
            "imageURL",
            ""
        ]