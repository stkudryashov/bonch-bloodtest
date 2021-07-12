from django.shortcuts import render
from django.views.generic import ListView

from .models import BloodTest
from .models import Analysis, Indicator


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

        if len(patronymic) == 0:
            patronymic = None

        user = BloodTest.objects.filter(
            personal_number=personal_number,
            name=name,
            surname=surname,
            patronymic=patronymic,
            birthday=birthday
        )

        if len(user) == 1:
            data = Analysis.objects.filter(
                user=user[0]
            )

            args['results'] = data

        else:
            args['results'] = user

    return render(request, 'mainapp/views/results.html', args)

from datetime import date
def detail(request):
    args = {}

    if 'detail' in request.POST:
        test_id = request.POST.get('detail')
        analysis = Analysis.objects.get(id=test_id)

        analysis_data = Indicator.objects.filter(
            analysis=analysis
        )

        labels = []
        data = []
        normals = []

        today = date.today()
        count_sick_ability(analysis_data, city_region=analysis.user.city.region_number, age=today.year-analysis.user.birthday.year, sex=analysis.user.sex)

        # for d in analysis_data:
        #     labels.append(d.normalIndicator.name)
        #     data.append(d.value)
        #     normals.append(d.normalIndicator.value)

        args['detail'] = analysis
        args['data'] = {"labels": labels, "data": data, "normals": normals}

    return render(request, 'mainapp/views/detail.html', args)


import pandas as pd


def count_sick_ability(analysis_data, city_region, age, sex):
    print(city_region, age, sex)
    df1 = pd.DataFrame(analysis_data.values())

    return df1
