from functools import reduce
import logging
import operator
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Customer, TicketDetails, TicketHistory
from . import search

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

def ticket_detail(request, pk):
    ticket = get_object_or_404(TicketDetails, pk=pk)
    return render(request, 'parature/ticket_detail.html', {'ticket': ticket})

def customer_detail(request, pk):
    customer = get_object_or_404(Customer, pk=pk)
    if request.GET.get('q'):
        query = request.GET['q']
        search_results = search.ticket_search(query, customer_id=pk)
        tickets = search_results['tickets']
        return render(request, 'parature/customer_detail.html', {'customer': customer, 'tickets': tickets, 'q': query})
    else:
        tickets = customer.ticketdetails_set.all().order_by('-id')
        return render(request, 'parature/customer_detail.html', {'customer': customer, 'tickets': tickets})

def comment_detail(request, pk):
    comment = get_object_or_404(TicketHistory, pk=pk)
    return render(request, 'parature/comment_detail.html', {'comment': comment})

def customer_search(request):
    if request.GET.get('q'):
        query = request.GET['q']
        search_hits = search.customer_search(query)
        customers = []
        for hit in search_hits:
            customers.append(Customer.objects.get(id=int(hit.meta.id)))
        customers = sorted(customers, key=lambda c: c.netid)
        return render(request, 'parature/customer_search.html', {'customers': customers, 'q': query})
    else:
        return render(request, 'parature/customer_search.html')

def ticket_search(request):
    if request.GET.get('q'):
        query = request.GET['q']
        result_limit = 200
        search_results = search.ticket_search(query, result_limit)
        if search_results['total_results'] > result_limit:
            messages.warning(request, u'Found %d tickets but I\'m only going to display the first %d because otherwise the server crashes. ಠ_ಠ' % (search_results['total_results'], result_limit))
        return render(request, 'parature/ticket_search.html', {'tickets': search_results['tickets'], 'q': query})
    else:
        return render(request, 'parature/ticket_search.html')

def csr_list(request):
    csrs = sorted(TicketHistory.objects.values_list('performed_by_csr', flat=True).distinct())
    return render(request, 'parature/csr_list.html', {'csrs': csrs})

def csr_detail(request, csr):
    Q_csr = Q(performed_by_csr__exact=csr)
    Q_csr_assigned = Q(assignedto__exact=csr)
    Q_comment = Q(action_name__exact='Post External Comment') | Q(action_name__exact='Post Internal Comment')
    Q_solution = Q(action_name__exact='Solve')

    solved_count = TicketHistory.objects.filter(Q_solution, Q_csr).values_list('ticket_id', flat=True).distinct().count()
    commented_count = TicketHistory.objects.filter(Q_comment, Q_csr).values_list('ticket_id', flat=True).distinct().count()
    touched_count = TicketHistory.objects.filter(Q_csr).values_list('ticket_id', flat=True).distinct().count()

    oldest_action = TicketHistory.objects.filter(Q_csr).filter(action_date__isnull=False).earliest('action_date')
    newest_action = TicketHistory.objects.filter(Q_csr).filter(action_date__isnull=False).latest('action_date')

    tickets_solved_list = TicketDetails.objects.filter(Q_csr_assigned).order_by('-ticketid')

    ticket_created_dates = tickets_solved_list.values_list('datecreated', flat=True)

    paginator = Paginator(tickets_solved_list, 10) # show 10 tickets per page
    page = request.GET.get('page')
    try:
        tickets_solved = paginator.page(page)
    except PageNotAnInteger:
        # if page is not an integer, deliver first page.
        tickets_solved = paginator.page(1)
    except EmptyPage:
        # if page is out of range (e.g. 9999), deliver last page of results.
        tickets_solved = paginator.page(paginator.num_pages)

    return render(request, 'parature/csr.html', {'csr': csr, 'solved_count': solved_count, 'commented_count': commented_count, 'touched_count': touched_count, 'oldest_action': oldest_action, 'newest_action': newest_action, 'tickets_solved': tickets_solved, 'ticket_created_dates': ticket_created_dates})

