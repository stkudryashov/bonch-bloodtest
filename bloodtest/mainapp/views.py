from django.shortcuts import render
from django.views.generic import ListView

from .models import BloodTest


class IndexHtml(ListView):
    model = BloodTest
    template_name = 'mainapp/views/index.html'


def search(request):
    return render(request, 'mainapp/forms/search.html')
