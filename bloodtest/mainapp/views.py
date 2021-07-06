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
        name = request.POST.get('name').strip()
        surname = request.POST.get('surname').strip()
        patronymic = request.POST.get('patronymic').strip()
        birthday = request.POST.get('birthday')

        data = BloodTest.objects.filter(
            personal_number=personal_number,
            name=name,
            surname=surname,
            patronymic=patronymic,
            birthday=birthday
        )

        args['results'] = data

    return render(request, 'mainapp/views/results.html', args)


def detail(request):
    args = {}

    if 'detail' in request.POST:
        test_id = request.POST.get('detail')
        data = BloodTest.objects.get(id=test_id)

        args['detail'] = data

    return render(request, 'mainapp/views/detail.html', args)
