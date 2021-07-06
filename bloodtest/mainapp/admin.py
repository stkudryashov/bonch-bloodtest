from django.contrib import admin

from .models import *


@admin.register(BloodTest)
class BloodTestAdmin(admin.ModelAdmin):
    list_display = ('personal_number', 'name', 'surname', 'patronymic', 'birthday', 'datetime')
    list_display_links = ('personal_number',)

    ordering = ['-datetime']
    search_fields = ['personal_number', 'name', 'surname', 'patronymic']
