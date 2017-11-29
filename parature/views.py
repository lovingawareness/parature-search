from django.shortcuts import render, get_object_or_404
from .models import TicketDetails, TicketHistory

def ticket_list(request):
    tickets = TicketDetails.objects.all()[:10]
    return render(request, 'parature/ticket_list.html', {'tickets': tickets})

def ticket_detail(request, pk):
    ticket = get_object_or_404(TicketDetails, pk=pk)
    return render(request, 'parature/ticket_detail.html', {'ticket': ticket})
