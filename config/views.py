from django.shortcuts import redirect
from django.shortcuts import render
from django.urls import reverse

from datetime import date


def index(request):
    if request.user.is_authenticated:
        today = date.today()
        response = redirect(reverse('expense-list', kwargs={
            'year': today.year,
            'month': today.month,
        }))

    else:
        response = render(request, 'index.html')

    return response
