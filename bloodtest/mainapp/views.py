import datetime

from django.shortcuts import render
from django.views.generic import ListView

from .models import *

from datetime import date, datetime
import pandas as pd


class IndexHtml(ListView):
    model = User
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

        user = User.objects.filter(
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


def detail(request):
    args = {}

    if 'detail' in request.POST:
        test_id = request.POST.get('detail')
        analysis = Analysis.objects.get(id=test_id)

        analysis_data = Indicator.objects.filter(analysis=analysis)
        analysis_user = analysis.user

        user_age = datetime.now().year - analysis_user.birthday.year
        if user_age < 30:
            age = 18
        elif user_age < 55:
            age = 45
        else:
            age = 65

        labels = []
        normals_min = []
        normals_max = []
        user_data = []

        info_name = []
        info_text = []

        for indicator in analysis_data:
            normals_data = Normals.objects.using('HealthCare').get(name=indicator.type, age=age)
            labels.append(indicator.type)
            if analysis_user.sex:
                normals_min.append(normals_data.min_male)
                normals_max.append(normals_data.max_male)
            else:
                normals_min.append(normals_data.min_female)
                normals_max.append(normals_data.max_female)
            user_data.append(indicator.value)

            normals_info = Info.objects.using('HealthCare').get(name=indicator.type)
            info_name.append(normals_info.translate)
            info_text.append(normals_info.text)

        data = zip(labels, normals_min, normals_max, user_data, info_name, info_text)

        args['data'] = data
        args['info'] = analysis.additional_info
        args['test'] = Normals.objects.using('HealthCare').all()

        today = date.today()
        count_sick_ability(analysis_data, city_region=analysis_user.city.region_number, age=user_age, sex=analysis_user.sex)

        # for d in analysis_data:
        #     labels.append(d.normalIndicator.name)
        #     data.append(d.value)
        #     normals.append(d.normalIndicator.value)

        args['detail'] = analysis

    return render(request, 'mainapp/views/detail.html', args)


def count_sick_ability(analysis_data, city_region, age, sex):
    df1 = pd.DataFrame(analysis_data.values())

    return df1
