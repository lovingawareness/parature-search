from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Customer, TicketDetails, TicketHistory

@login_required
def ticket_detail(request, pk):
    ticket = get_object_or_404(TicketDetails, pk=pk)
    return render(request, 'parature/ticket_detail.html', {'ticket': ticket})

@login_required
def customer_detail(request, pk):
    customer = get_object_or_404(Customer, pk=pk)
    tickets = customer.ticketdetails_set.all()
    return render(request, 'parature/customer_detail.html', {'customer': customer, 'tickets': tickets})

@login_required
def comment_detail(request, pk):
    comment = get_object_or_404(TicketHistory, pk=pk)
    return render(request, 'parature/comment_detail.html', {'comment': comment})

@login_required
def ticket_search(request):
    if 'q' in request.GET and request.GET['q']:
        q = request.GET['q']
        tickets = TicketDetails.objects.filter(details__icontains=q).order_by('id')
        return render(request, 'parature/ticket_search.html', {'tickets': tickets, 'query': q})
    else:
        return render(request, 'parature/ticket_search.html')
