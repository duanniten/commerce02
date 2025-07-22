from .models import Bid, Listing, Comment

def getCurrentBidValue(listing: Listing):
    biger_bid = Bid.objects.filter(listing = listing).order_by('-value').first()
    if biger_bid:
        biger_bid_value = biger_bid.value
    else:
        biger_bid_value = listing.initBid
    return biger_bid_value, biger_bid

def getComments(listing: Listing):
    comments = Comment.objects.filter(listing = listing)
    return comments