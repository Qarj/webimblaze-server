from django.urls import path

from . import views

app_name = 'server'

urlpatterns = [
    # ex: /server/
    path('', views.index, name='index'),
]