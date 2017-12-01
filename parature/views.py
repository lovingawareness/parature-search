from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from .models import Customer, TicketDetails, TicketHistory

def index(request):
    return HttpResponse("You have reached the index.")

def ticket_detail(request, pk):
    ticket = get_object_or_404(TicketDetails, pk=pk)
    return render(request, 'parature/ticket_detail.html', {'ticket': ticket})

def customer_detail(request, pk):
    customer = get_object_or_404(Customer, pk=pk)
    tickets = customer.ticketdetails_set.all()
    return render(request, 'parature/customer_detail.html', {'customer': customer, 'tickets': tickets})

def ticket_search(request):
    if 'q' in request.GET and request.GET['q']:
        q = request.GET['q']
        tickets = TicketDetails.objects.filter(details__contains=q).order_by('-datecreated')
        return render(request, 'parature/ticket_list_with_search.html', {'tickets': tickets, 'query': q})
    else:
        return render(request, 'parature/ticket_list_with_search.html')

def customer_search(request):
    if 'q' in request.GET and request.GET['q']:
        q = request.GET['q']
        customers = Customer.objects.filter(netid__contains=q).order_by('netid')
        return render(request, 'parature/customer_list_and_search.html', {'customers': customers, 'query': q})
    else:
        return render(request, 'parature/customer_list_and_search.html')
