from django.contrib import admin
from .models import Customer, TicketDetails, TicketHistory

admin.site.register(Customer)
admin.site.register(TicketDetails)
admin.site.register(TicketHistory)
