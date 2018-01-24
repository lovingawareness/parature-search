from functools import reduce
import operator
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from .models import Customer, TicketDetails, TicketHistory

def ticket_detail(request, pk):
    ticket = get_object_or_404(TicketDetails, pk=pk)
    return render(request, 'parature/ticket_detail.html', {'ticket': ticket})

def customer_detail(request, pk):
    customer = get_object_or_404(Customer, pk=pk)
    tickets = customer.ticketdetails_set.all().order_by('-id')
    return render(request, 'parature/customer_detail.html', {'customer': customer, 'tickets': tickets})

def comment_detail(request, pk):
    comment = get_object_or_404(TicketHistory, pk=pk)
    return render(request, 'parature/comment_detail.html', {'comment': comment})

def customer_search(request):
    query_filters = []
    queries = {'Name': '', 'NetID': '', 'Email': ''}
    if request.GET.get('q_netid'):
        queries['NetID'] = request.GET.get('q_netid')
        query_filters.append(Q(netid__icontains=queries['NetID']))
    if request.GET.get('q_name'):
        queries['Name'] = request.GET.get('q_name')
        query_filters.append(Q(first_name__icontains=queries['Name']) or Q(last_name__icontains=queries['Name']))
    if request.GET.get('q_email'):
        queries['Email'] = request.GET.get('q_email')
        query_filters.append(Q(email__icontains=queries['Email']))
    if len(query_filters) > 0:
        customers = Customer.objects.filter(reduce(operator.and_, query_filters)).distinct().order_by('netid')
        query_string = ', '.join((k + ':' + v for k,v in queries.items()))
        return render(request, 'parature/customer_search.html', {'customers': customers, 'query_string': query_string, 'queries': queries})
    else:
        return render(request, 'parature/customer_search.html')

def csr_list(request):
    csrs = sorted(TicketHistory.objects.values_list('performed_by_csr', flat=True).distinct())
    return render(request, 'parature/csr_list.html', {'csrs': csrs})

def csr_detail(request, csr):
    Q_csr = Q(performed_by_csr__exact=csr)
    Q_comment = Q(action_name__exact='Post External Comment') | Q(action_name__exact='Post Internal Comment')
    Q_solution = Q(action_name__exact='Solve')

    solved_count = TicketHistory.objects.filter(Q_solution, Q_csr).values_list('ticket_id', flat=True).distinct().count()
    commented_count = TicketHistory.objects.filter(Q_comment, Q_csr).values_list('ticket_id', flat=True).distinct().count()
    touched_count = TicketHistory.objects.filter(Q_csr).values_list('ticket_id', flat=True).distinct().count()

    oldest_action = TicketHistory.objects.filter(Q_csr).filter(action_date__isnull=False).earliest('action_date')
    newest_action = TicketHistory.objects.filter(Q_csr).filter(action_date__isnull=False).latest('action_date')

    tickets_solved_list = TicketDetails.objects.filter(Q(assignedto__exact=csr)).order_by('-ticketid')
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

    return render(request, 'parature/csr.html', {'csr': csr, 'solved_count': solved_count, 'commented_count': commented_count, 'touched_count': touched_count, 'oldest_action': oldest_action, 'newest_action': newest_action, 'tickets_solved': tickets_solved})

