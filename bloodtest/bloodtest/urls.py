from django.contrib import admin
from django.urls import path, include

from mainapp import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('mainapp.urls')),
    path('results/', views.results)
]
