from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from .models import TicketDetails, TicketHistory


def ticket_list(request):
    tickets = TicketDetails.objects.order_by('datecreated')[:20]
    return render(request, 'parature/ticket_list.html', {'tickets': tickets})

def ticket_detail(request, pk):
    ticket = get_object_or_404(TicketDetails, pk=pk)
    return render(request, 'parature/ticket_detail.html', {'ticket': ticket})

def search_form(request):
    return render(request, 'parature/search_form.html')

def search(request):
    if 'q' in request.GET and request.GET['q']:
        q = request.GET['q']
        tickets = TicketDetails.objects.filter(details__contains=q).order_by('datecreated')
        return render(request, 'parature/ticket_list.html', {'tickets': tickets, 'query': q})
    else:
        return HttpResponse('Please submit a search term.')
