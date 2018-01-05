from functools import reduce
import operator
from django.shortcuts import render, get_object_or_404
from django.db.models import Q
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
        query = request.GET['q']
        search_fields = {'ticket_details': request.GET.get('search_ticket_details') == 'on',
                        'ticket_summary': request.GET.get('search_ticket_summary') == 'on',
                        'ticket_solution': request.GET.get('search_ticket_solution') == 'on',
                        'ticket_comments': request.GET.get('search_ticket_history') == 'on'}
        query_filters = []
        if search_fields['ticket_details']:
            query_filters.append(Q(details__icontains=query))
        if search_fields['ticket_summary']:
            query_filters.append(Q(summary__icontains=query))
        if search_fields['ticket_solution']:
            query_filters.append(Q(solution__icontains=query))
        if search_fields['ticket_comments']:
            query_filters.append(Q(tickethistory__comments__icontains=query))
        tickets = TicketDetails.objects.filter(reduce(operator.or_, query_filters)).distinct().order_by('-id')
        return render(request, 'parature/ticket_search.html', {'tickets': tickets, 'query': query})
    else:
        return render(request, 'parature/ticket_search.html')
