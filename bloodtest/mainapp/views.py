from django.shortcuts import render
from django.views.generic import ListView

from .models import BloodTest


class IndexHtml(ListView):
    model = BloodTest
    template_name = 'mainapp/views/index.html'


def search(request):
    return render(request, 'mainapp/forms/search.html')


def results(request):
    args = {}

    if 'results' in request.POST:
        personal_number = request.POST.get('personal_number')
        data = BloodTest.objects.filter(personal_number=personal_number)

        args['results'] = data

    return render(request, 'mainapp/views/results.html', args)
