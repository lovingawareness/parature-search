from django.shortcuts import render
from django.views.generic import ListView
from django_currentuser.middleware import get_current_authenticated_user
from .models import Record

class MyHistoryList(ListView):
    model = Record

    def get_queryset(self):
        return Record.objects.filter(user=get_current_authenticated_user()).order_by('-created_at')
