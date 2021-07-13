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

        result = count_sick_ability(
            analysis_data,
            city_region=analysis_user.city.region_number,
            age=age,
            sex=analysis_user.sex
        )

        if result < 0:
            args['result'] = 'Мало информации'
        else:
            if result > 100:
                result = 100
            args['result'] = str(result) + '%'

        args['detail'] = analysis

    return render(request, 'mainapp/views/detail.html', args)


def count_sick_ability(analysis_data, city_region, age, sex):
    df = pd.read_csv("covid19-russia.csv")
    d_region = pd.read_csv("regions-info.csv")

    try:
        pop = d_region.loc[d_region["Region_ID"] == city_region, ["Population"]]
        pop = pd.Series(pop["Population"][:1]).item()
        bed_pop = df.loc[df["Region_ID"] == city_region, ["Date", "Confirmed"]]
        bed_pop.sort_values(by=["Date"], ascending=False, inplace=True)
        bed_pop = pd.Series(bed_pop["Confirmed"][:1]).item()
        d_normal = pd.read_csv("Health.csv")
        d_anal = pd.DataFrame(analysis_data.values())
        d_anal = d_anal[["type", "value"]]
        d_normal = d_normal[d_normal["age"] == age]
        print(d_normal)
        d_normal.drop(["age"], axis=1, inplace=True)

        if sex == 1:
            d_normal.drop(["min_female", "max_female"], axis=1, inplace=True)
            d_normal.rename(columns={"min_male": "min", "max_male": "max"}, inplace=True)
        elif sex == 0:
            d_normal.drop(["min_male", "max_male"], axis=1, inplace=True)
            d_normal.rename(columns={"min_female": "min", "max_female": "max"}, inplace=True)
        else:
            return -1
        d_normal.index = d_normal["name"]
        status = 0
        for name, value in zip(d_anal["type"], d_anal["value"]):
            if value > d_normal.loc[name, ["max"]][0]:
                print("max")
            elif value < d_normal.loc[name, ["min"]][0]:
                print("min")
            else:
                print("normal")
                status += 1 / d_anal["value"].size
        if status == 0:
            return 100
        return round((bed_pop / pop) / status * 100, 4)
    except KeyError as e:
        return -1
