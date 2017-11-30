from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from .models import TicketDetails, TicketHistory


def ticket_detail(request, pk):
    ticket = get_object_or_404(TicketDetails, pk=pk)
    return render(request, 'parature/ticket_detail.html', {'ticket': ticket})

def index(request):
    if 'q' in request.GET and request.GET['q']:
        q = request.GET['q']
        tickets = TicketDetails.objects.filter(details__contains=q).order_by('-datecreated')
        return render(request, 'parature/ticket_list_with_search.html', {'tickets': tickets, 'query': q})
    else:
        return render(request, 'parature/ticket_list_with_search.html')
