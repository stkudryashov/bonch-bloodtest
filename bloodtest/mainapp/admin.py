from django.contrib import admin

from .models import *

class AnalysisInLine(admin.TabularInline):
    model = Analysis

class IndicatorsInLine(admin.TabularInline):
    model = Indicator

@admin.register(BloodTest)
class BloodTestAdmin(admin.ModelAdmin):
    list_display = ('personal_number', 'name', 'surname', 'patronymic', 'birthday')
    list_display_links = ('personal_number',)

    search_fields = ['personal_number', 'name', 'surname', 'patronymic']

    inlines = [
        AnalysisInLine
    ]

@admin.register(Analysis)
class AnalysisAdmin(admin.ModelAdmin):

    inlines = [
        IndicatorsInLine
    ]

    ordering = ['-datetime']


admin.site.register(Indicator)

admin.site.register(City)