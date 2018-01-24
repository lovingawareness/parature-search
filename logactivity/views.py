from django.shortcuts import render
from django.views.generic import ListView
from .models import Record

class MySearchesList(ListView):
    model = Record

    def get_context_data(self, **kwargs):
        context = super(MySearchesList, self).get_context_data(**kwargs)
        self.queryset = Record.objects.filter(user=self.request.user)
        self.context_object_name = 'my_searches'
        return context
