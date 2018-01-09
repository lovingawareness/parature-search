from haystack import indexes
from .models import TicketDetails, TicketHistory, Customer

class TicketIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)

    def prepare_tickethistorys(self, object):
        return [tickethistory.comments for tickethistory in object.tickethistory.all()]

    def get_model(self):
        return TicketDetails

    def load_all_queryset(self):
        return TicketDetails.objects.all().select_related()
