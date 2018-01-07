from haystack import indexes
from .models import TicketDetails, TicketHistory, Customer

class TicketIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    summary = indexes.CharField(model_attr='summary')

    def get_model(self):
        return TicketDetails
