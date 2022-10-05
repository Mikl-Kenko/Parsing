from django.urls import path

from .views import pars_user, ajax, list_user, get_user

app_name = 'main'

urlpatterns = [
    path('', pars_user, name='pars_user'),
    path('ajax/', ajax, name="ajax"),
    path('list_user/', list_user, name="list_user"),
    path('user/<int:id>/', get_user, name='get_user')
    ]
